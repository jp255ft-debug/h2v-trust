"""
Script para testar a emissao do Soulbound Token (SBT) na blockchain
Chama diretamente o contrato GreenHydrogenSBT via Web3
"""
import json
import sys
import os
from web3 import Web3

# Forcar UTF-8 no Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Configuracoes
RPC_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0xa513E6E4b8f2a923D98304ec87F64353C4D5C853"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# ABI real do contrato (extraido do artifact compilado)
CONTRACT_ABI = json.loads('[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"address","name":"_batchRegistry","type":"address"},{"internalType":"address","name":"_complianceVerifier","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721IncorrectOwner","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721InsufficientApproval","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC721InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"ERC721InvalidOperator","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721InvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC721InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC721InvalidSender","type":"error"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721NonexistentToken","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldRegistry","type":"address"},{"indexed":true,"internalType":"address","name":"newRegistry","type":"address"}],"name":"BatchRegistryUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"address","name":"consumedBy","type":"address"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"CertificateConsumed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":true,"internalType":"bytes32","name":"batchId","type":"bytes32"},{"indexed":true,"internalType":"address","name":"producer","type":"address"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"sizeKg","type":"uint256"},{"indexed":false,"internalType":"bool","name":"isCompliant","type":"bool"}],"name":"CertificateMinted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldVerifier","type":"address"},{"indexed":true,"internalType":"address","name":"newVerifier","type":"address"}],"name":"ComplianceVerifierUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"MetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"batchRegistry","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"batchToTokenId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"calculateCarbonSavings","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"certificateData","outputs":[{"internalType":"bytes32","name":"batchId","type":"bytes32"},{"internalType":"address","name":"producer","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"uint256","name":"sizeKg","type":"uint256"},{"internalType":"uint256","name":"ghgEmissions","type":"uint256"},{"internalType":"uint256","name":"waterConsumption","type":"uint256"},{"internalType":"bool","name":"isCompliant","type":"bool"},{"internalType":"bytes32","name":"complianceHash","type":"bytes32"},{"internalType":"bool","name":"isConsumed","type":"bool"},{"internalType":"uint256","name":"consumedAt","type":"uint256"},{"internalType":"address","name":"consumedBy","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"complianceVerifier","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"consumeCertificate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getCertificateData","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bool","name":"","type":"bool"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bool","name":"","type":"bool"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"getOwnerCertificates","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"producer","type":"address"}],"name":"getProducerCertificates","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"batchId","type":"bytes32"}],"name":"getTokenIdForBatch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalCertificates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"isValidCertificate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"batchId","type":"bytes32"},{"internalType":"address","name":"producer","type":"address"},{"internalType":"string","name":"_tokenURI","type":"string"}],"name":"mintCertificate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"ownerCertificates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"producerCertificates","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newRegistry","type":"address"}],"name":"updateBatchRegistry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newVerifier","type":"address"}],"name":"updateComplianceVerifier","outputs":[],"stateMutability":"nonpayable","type":"function"}]')


def main():
    print("=" * 60)
    print("TESTE DE EMISSAO DO SOULBOUND TOKEN (SBT)")
    print("=" * 60)
    
    # Conectar ao Hardhat
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("[ERRO] Nao foi possivel conectar ao Hardhat node em", RPC_URL)
        sys.exit(1)
    
    print("[OK] Conectado ao Hardhat node. Block:", w3.eth.block_number)
    
    # Verificar contrato
    checksum_address = w3.to_checksum_address(CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=checksum_address, abi=CONTRACT_ABI)
    
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        total = contract.functions.getTotalCertificates().call()
        print("[OK] Contrato:", name, "(" + symbol + ")")
        print("     Total Certificates:", total)
        print("     Endereco:", checksum_address)
    except Exception as e:
        print("[ERRO] ao ler contrato:", e)
        sys.exit(1)
    
    # Preparar mint
    account = w3.eth.account.from_key(PRIVATE_KEY)
    producer = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"  # Conta #2 do Hardhat
    
    batch_id_str = "BATCH-TEST-001"
    batch_id_bytes = w3.keccak(text=batch_id_str)
    
    token_metadata = {
        "name": "Green Hydrogen Certificate - " + batch_id_str,
        "description": "Soulbound Token (SBT) certifying green hydrogen production",
        "attributes": [
            {"trait_type": "Batch ID", "value": batch_id_str},
            {"trait_type": "Producer", "value": producer},
            {"trait_type": "Certificate Type", "value": "Green Hydrogen SBT"},
            {"trait_type": "Compliance Standard", "value": "CBAM 2026"}
        ]
    }
    token_uri = "data:application/json;charset=utf-8," + json.dumps(token_metadata)
    
    print()
    print("Preparando mint do SBT...")
    print("   Batch ID:", batch_id_str)
    print("   Producer:", producer)
    print("   Token URI:", token_uri[:80] + "...")
    
    # Estimar gas
    try:
        estimated_gas = contract.functions.mintCertificate(
            batch_id_bytes, producer, token_uri
        ).estimate_gas({'from': account.address})
        gas_limit = int(estimated_gas * 1.5)
        print("   Gas estimado:", estimated_gas, "usando:", gas_limit)
    except Exception as e:
        print("   [AVISO] Estimativa de gas falhou:", e)
        gas_limit = 2000000
    
    # Construir e enviar transacao
    nonce = w3.eth.get_transaction_count(account.address)
    print("   Nonce:", nonce)
    
    tx = contract.functions.mintCertificate(
        batch_id_bytes, producer, token_uri
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': gas_limit,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print()
    print("[...] Transacao enviada! Hash:", tx_hash.hex())
    
    # Aguardar confirmacao
    print("   Aguardando confirmacao...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt.status == 1:
        print("[OK] TRANSACAO CONFIRMADA!")
        print("   Block:", receipt.blockNumber)
        print("   Gas usado:", receipt.gasUsed)
        
        # Extrair token ID do evento Transfer
        transfer_event_hash = w3.keccak(text="Transfer(address,address,uint256)").hex()
        token_id = None
        
        for log in receipt.logs:
            if len(log.topics) >= 4 and log.topics[0].hex() == transfer_event_hash:
                token_id = int.from_bytes(log.topics[3], byteorder='big')
                break
        
        if token_id is not None:
            print()
            print(">>> TOKEN ID:", token_id)
            print(">>> TX HASH:", tx_hash.hex())
            
            # Verificar o token mintado
            owner = contract.functions.ownerOf(token_id).call()
            token_uri_onchain = contract.functions.tokenURI(token_id).call()
            print()
            print("Verificacao on-chain:")
            print("   Owner:", owner)
            print("   Token URI:", token_uri_onchain[:100] + "...")
            
            # Verificar total supply
            new_total = contract.functions.getTotalCertificates().call()
            print("   Total Certificates:", new_total)
            
            print()
            print("=" * 60)
            print("SBT EMITIDO COM SUCESSO!")
            print("=" * 60)
        else:
            print("[ERRO] Nao foi possivel extrair o token ID do receipt")
    else:
        print("[ERRO] TRANSACAO REVERTIDA!")
        try:
            tx_data = w3.eth.call({
                'from': account.address,
                'to': checksum_address,
                'data': tx['data']
            })
            print("   Reason:", tx_data.hex())
        except Exception as e:
            print("   Erro:", e)


if __name__ == "__main__":
    main()
