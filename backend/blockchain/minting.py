import logging
import json
import asyncio
from web3 import Web3
from blockchain.web3_client import get_contract, get_w3
from config import settings

logger = logging.getLogger(__name__)


def extract_token_id_from_receipt(tx_receipt, contract_address):
    """
    Extrai o token ID diretamente dos tópicos do evento Transfer (ERC-721).
    
    O evento Transfer(from, to, tokenId) é emitido obrigatoriamente pelo ERC-721
    quando um token é criado via _safeMint.
    
    - topic[0]: hash da assinatura do evento Transfer(address,address,uint256)
    - topic[1]: from (address indexed, 0x0 para mint)
    - topic[2]: to (address indexed)
    - topic[3]: tokenId (uint256 indexed)
    """
    transfer_event_hash = Web3.keccak(text="Transfer(address,address,uint256)").hex()
    
    # Acessar logs do receipt (pode ser AttributeDict ou dict)
    receipt_logs = getattr(tx_receipt, 'logs', [])
    if not receipt_logs and isinstance(tx_receipt, dict):
        receipt_logs = tx_receipt.get('logs', [])
    
    for log in receipt_logs:
        # Extrair address do log
        log_address = getattr(log, 'address', None)
        if log_address is None and isinstance(log, dict):
            log_address = log.get('address', '')
        
        # Extrair topics do log
        topics = getattr(log, 'topics', [])
        if not topics and isinstance(log, dict):
            topics = log.get('topics', [])
        
        # Verificar se é do nosso contrato e se é evento Transfer
        if (log_address and log_address.lower() == contract_address.lower() and 
            len(topics) >= 4 and 
            topics[0].hex() if hasattr(topics[0], 'hex') else str(topics[0]) == transfer_event_hash):
            
            # tokenId está no topic[3] (uint256 indexed)
            token_id_topic = topics[3]
            if isinstance(token_id_topic, bytes):
                token_id = int.from_bytes(token_id_topic, byteorder='big')
            elif isinstance(token_id_topic, str) and token_id_topic.startswith('0x'):
                token_id = int(token_id_topic, 16)
            else:
                token_id = int(token_id_topic)
            
            logger.info(f"Token ID extracted from Transfer event: {token_id}")
            return token_id
    
    # Fallback: tentar extrair de qualquer log com topics >= 2
    # (para contratos que podem ter eventos personalizados)
    for log in receipt_logs:
        topics = getattr(log, 'topics', [])
        if not topics and isinstance(log, dict):
            topics = log.get('topics', [])
        
        if len(topics) >= 2:
            token_id_topic = topics[1]
            if isinstance(token_id_topic, bytes):
                token_id = int.from_bytes(token_id_topic, byteorder='big')
            elif isinstance(token_id_topic, str) and token_id_topic.startswith('0x'):
                token_id = int(token_id_topic, 16)
            else:
                token_id = int(token_id_topic)
            
            if token_id > 0:
                logger.info(f"Token ID extracted from fallback (topic[1]): {token_id}")
                return token_id
    
    raise ValueError("Token ID not found in transaction receipt")


async def mint_certificate_on_chain(
    batch_id: str, 
    producer_address: str, 
    metadata: dict
):
    """
    Mint a new SBT certificate on-chain with proper metadata packaging
    
    Args:
        batch_id: Batch identifier (string)
        producer_address: Ethereum address of the producer
        metadata: Dictionary containing certificate metadata (emissions, water source, etc.)
    
    Returns:
        Tuple of (transaction_hash, token_id)
    """
    w3 = get_w3()
    contract = get_contract()
    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Converter batch_id para bytes32 (hexadecimal)
    if batch_id.startswith('0x'):
        if len(batch_id) > 66:
            batch_id = batch_id[:66]
        batch_id_bytes = w3.to_bytes(hexstr=batch_id)
    else:
        batch_id_bytes = w3.keccak(text=batch_id)
    
    # Garantir que temos exatamente 32 bytes
    if len(batch_id_bytes) > 32:
        batch_id_bytes = batch_id_bytes[:32]
    elif len(batch_id_bytes) < 32:
        batch_id_bytes = batch_id_bytes.ljust(32, b'\0')
    
    # Criar token URI com metadados no padrão ERC-721
    token_metadata = {
        "name": f"Green Hydrogen Certificate - Batch {batch_id[:16]}...",
        "description": "Soulbound Token (SBT) certifying green hydrogen production compliant with CBAM regulations",
        "image": "https://h2v-trust.com/certificate-badge.png",
        "external_url": f"https://h2v-trust.com/certificates/{batch_id}",
        "attributes": [
            {"trait_type": "Batch ID", "value": batch_id},
            {"trait_type": "Producer", "value": producer_address},
            {"trait_type": "Certificate Type", "value": "Green Hydrogen SBT"},
            {"trait_type": "Compliance Standard", "value": "CBAM 2026"}
        ]
    }
    
    if metadata:
        for key, value in metadata.items():
            if key not in ["name", "description", "image", "external_url"]:
                token_metadata["attributes"].append({
                    "trait_type": key.replace("_", " ").title(),
                    "value": str(value)
                })
    
    token_uri = f"data:application/json;charset=utf-8,{json.dumps(token_metadata)}"
    
    # Estimar gas
    try:
        estimated_gas = contract.functions.mintCertificate(
            batch_id_bytes,
            producer_address,
            token_uri
        ).estimate_gas({'from': account.address})
        gas_limit = int(estimated_gas * 1.5)
        logger.info(f"Estimated gas: {estimated_gas}, using: {gas_limit}")
    except Exception as e:
        logger.warning(f"Gas estimation failed: {e}, using default 2M gas")
        gas_limit = 2000000
    
    tx = contract.functions.mintCertificate(
        batch_id_bytes,
        producer_address,
        token_uri
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': gas_limit,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_tx = account.sign_transaction(tx)
    raw_tx = signed_tx.raw_transaction
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    
    # wait_for_transaction_receipt é síncrono e bloqueia o event loop
    # Executar em thread separada para não travar o FastAPI
    receipt = await asyncio.to_thread(
        w3.eth.wait_for_transaction_receipt, tx_hash, timeout=120
    )
    
    if receipt.status == 0:
        logger.error("Transaction reverted on-chain")
        raise ValueError("Blockchain transaction reverted on-chain. Verify if the contract is deployed and valid.")
    
    # Extrair token ID usando o método robusto (evento Transfer do ERC-721)
    contract_address = w3.to_checksum_address(settings.CONTRACT_ADDRESS)
    
    try:
        token_id = extract_token_id_from_receipt(receipt, contract_address)
    except ValueError:
        # Fallback: tentar via process_receipt do CertificateMinted
        logger.warning("Transfer event not found, trying CertificateMinted event...")
        try:
            logs = contract.events.CertificateMinted().process_receipt(receipt)
            if logs:
                token_id = logs[0]['args']['tokenId']
                logger.info(f"Token ID extracted from CertificateMinted event: {token_id}")
            else:
                raise ValueError("No CertificateMinted events found")
        except Exception as e:
            logger.error(f"All extraction methods failed: {e}")
            raise ValueError("Failed to extract token ID from blockchain transaction")
    
    # Handle both HexBytes and string tx_hash
    if hasattr(tx_hash, 'hex'):
        tx_hash_hex = tx_hash.hex()
    else:
        tx_hash_hex = tx_hash
    
    logger.info(f"Certificate minted: token_id={token_id}, tx_hash={tx_hash_hex}")
    return tx_hash_hex, token_id
