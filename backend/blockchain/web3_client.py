from web3 import Web3
try:
    from web3.middleware import ExtraDataToPOAMiddleware
except ImportError:
    # web3.py >= 7.x renamed ExtraDataToPOAMiddleware
    from web3.middleware import geth_poa_middleware as ExtraDataToPOAMiddleware
import json
import os
import logging
import sys
# Ensure backend package is importable
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
from config import settings

logger = logging.getLogger(__name__)

w3 = None
contract = None
_initialized = False

def init_web3(force_reload=False):
    """Initialize Web3 connection with PoA middleware for Hardhat"""
    global w3, contract, _initialized
    
    if _initialized and not force_reload:
        return w3, contract
    
    if force_reload:
        logger.info("Forcing Web3 re-initialization...")
        w3 = None
        contract = None
        _initialized = False
    
    # Check if mock mode is enabled
    if settings.MOCK_MODE:
        logger.info("MOCK_MODE enabled. Using mock Web3 connection.")
        
        # --- Classe MockMiddleware ---
        class MockMiddleware:
            def inject(self, *args, **kwargs):
                pass
        
        # --- Classe MockFilter ---
        class MockFilter:
            def get_all_entries(self):
                return []
        
        # --- Classe MockEvent ---
        class MockEvent:
            _token_id_counter = 1000  # Start at 1000 to avoid conflicts with existing data
            
            def create_filter(self, *args, **kwargs):
                return MockFilter()
            
            def process_receipt(self, receipt):
                """Mock process_receipt that returns a list of log entries."""
                # Simula um log de evento CertificateMinted
                # Usa timestamp para garantir token_id único mesmo após reinicialização
                import time
                import random
                # Combina timestamp (milissegundos) com número aleatório para garantir unicidade
                token_id = int(time.time() * 1000000) + random.randint(1, 1000)
                return [{
                    'args': {
                        'tokenId': token_id,
                        'producer': '0x' + '0' * 40,
                        'emissions': 2800000,  # 2.8 * 1e6
                        'batchSize': 1000
                    }
                }]
        
        # --- Classe MockEvents ---
        class MockEvents:
            def CertificateMinted(self):
                return MockEvent()
            
            def CertificateConsumed(self):
                return MockEvent()
        
        # --- Classe MockFunction ---
        class MockFunction:
            def __call__(self, *args, **kwargs):
                return self
            
            def transact(self, *args, **kwargs):
                return "0x" + "0" * 64
            
            def call(self, *args, **kwargs):
                return 1
            
            def build_transaction(self, transaction_dict):
                return {
                    "to": "0x" + "0" * 40,
                    "value": 0,
                    "gas": 200000,
                    "gasPrice": 1000000000,
                    "nonce": 0,
                    "chainId": 31337,
                    "data": "0x" + "0" * 64
                }
        
        # --- Classe MockFunctions ---
        class MockFunctions:
            def __init__(self):
                self.mintCertificate = MockFunction()
                self.getCertificate = MockFunction()
                self.consumeCertificate = MockFunction()
        
        # --- Classe MockContract ---
        class MockContract:
            def __init__(self):
                self.functions = MockFunctions()
                self.events = MockEvents()
        
        # --- Classe MockEth (CORRIGIDA) ---
        class MockEth:
            def __init__(self):
                self.chain_id = 31337
                self.contract = lambda address, abi: MockContract()
                
                # Account mock (para assinar transações)
                class AccountClass:
                    @staticmethod
                    def from_key(private_key):
                        class AccountInstance:
                            address = "0x" + "0" * 40
                            def sign_transaction(self, tx_dict):
                                class SignedTx:
                                    rawTransaction = b'\x00' * 32
                                return SignedTx()
                        return AccountInstance()
                self.account = AccountClass
            
            @property
            def gas_price(self):
                """Mock gas price (1 Gwei)."""
                return 1000000000
            
            def get_gas_price(self):
                """Compatibility method."""
                return self.gas_price
            
            def get_transaction_count(self, address):
                return 0
            
            def send_raw_transaction(self, signed_tx):
                return "0x" + "0" * 64
            
            def wait_for_transaction_receipt(self, tx_hash, timeout=120):
                """Mock receipt that includes event logs for CertificateMinted."""
                import time
                import random
                # Generate a deterministic token_id based on timestamp
                token_id = int(time.time() * 1000000) + random.randint(1, 1000)
                
                class MockLog:
                    """Mock event log entry matching CertificateMinted event signature."""
                    def __init__(self):
                        self.address = "0x" + "0" * 40
                        self.blockHash = b'\x00' * 32
                        self.blockNumber = 123456
                        self.data = "0x" + "0" * 64
                        self.logIndex = 0
                        self.removed = False
                        self.topics = [
                            # keccak256("CertificateMinted(uint256,bytes32,address,uint256,uint256,bool)")
                            "0x" + "0" * 64,
                            # tokenId (indexed)
                            "0x" + format(token_id, '064x'),
                            # batchId (indexed)
                            "0x" + "0" * 64,
                            # producer (indexed)
                            "0x" + "0" * 40 + "000000000000000000000000",
                        ]
                        self.transactionHash = tx_hash
                        self.transactionIndex = 0
                    
                    def __getitem__(self, key):
                        """Allow dict-style access for process_receipt compatibility."""
                        if key == 'args':
                            return type('Args', (), {
                                'tokenId': token_id,
                                'batchId': b'\x00' * 32,
                                'producer': '0x' + '0' * 40,
                                'timestamp': int(time.time()),
                                'sizeKg': 1000,
                                'isCompliant': True
                            })()
                        raise KeyError(key)
                
                class MockReceipt:
                    status = 1
                    transactionHash = tx_hash
                    blockNumber = 123456
                    gasUsed = 21000
                    logs = [MockLog()]
                
                return MockReceipt()
        
        # --- Classe MockWeb3 ---
        class MockWeb3:
            def __init__(self):
                self.eth = MockEth()
                self.is_connected = lambda: True
                self.middleware_onion = MockMiddleware()
            
            def to_checksum_address(self, address):
                return address
            
            def keccak(self, text=None, hexstr=None):
                return b"\x00" * 32
            
            def to_bytes(self, hexstr=None, text=None):
                if hexstr:
                    return bytes.fromhex(hexstr[2:] if hexstr.startswith("0x") else hexstr)
                elif text:
                    return text.encode()
                return b""
        
        w3 = MockWeb3()
        contract = w3.eth.contract("0x" + "0" * 40, abi=[])
        _initialized = True
        logger.info("Mock Web3 initialized successfully")
        return w3, contract
    
    try:
        rpc_url = settings.POLYGON_RPC_URL
        logger.info(f"Initializing Web3 connection to: {rpc_url}")
        
        w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 30}))
        
        if not w3.is_connected():
            logger.error(f"Failed to connect to RPC: {rpc_url}")
            raise ConnectionError(f"Cannot connect to RPC: {rpc_url}")
        
        logger.info(f"Connected to blockchain network. Chain ID: {w3.eth.chain_id}")
        
        if "localhost" in rpc_url or "127.0.0.1" in rpc_url or "8545" in rpc_url:
            logger.info("Injecting PoA middleware for Hardhat/local network")
            w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        contract_address = settings.CONTRACT_ADDRESS
        if contract_address:
            logger.info(f"Loading contract at address: {contract_address}")
            
            # Prioridade: primeiro o JSON compilado do Hardhat (mais completo)
            possible_paths = [
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "contracts",
                    "artifacts",
                    "contracts",
                    "GreenHydrogenSBT.sol",
                    "GreenHydrogenSBT.json"
                ),
                # Caminho local dentro do backend (cópia do ABI)
                os.path.join(
                    os.path.dirname(__file__),
                    "GreenHydrogenSBT.json"
                ),
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "contracts",
                    "GreenHydrogenSBT.json"
                ),
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "contracts",
                    "compile_out.txt"
                )
            ]
            
            abi = None
            abi_path = None
            
            for path in possible_paths:
                if os.path.exists(path):
                    abi_path = path
                    logger.info(f"Found ABI at: {path}")
                    try:
                        with open(path, "r") as f:
                            if path.endswith(".json"):
                                abi_data = json.load(f)
                                abi = abi_data.get("abi", [])
                                if not abi and isinstance(abi_data, list):
                                    abi = abi_data
                            else:
                                abi = json.loads(f.read())
                        break
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.warning(f"Failed to parse ABI from {path}: {e}")
                        continue
            
            if abi is None:
                logger.error("No valid ABI file found. Contract interactions will fail.")
                logger.info("Please compile contracts with: cd contracts && npx hardhat compile")
            else:
                if not w3.is_address(contract_address):
                    logger.error(f"Invalid contract address: {contract_address}")
                else:
                    contract = w3.eth.contract(
                        address=w3.to_checksum_address(contract_address),
                        abi=abi
                    )
                    logger.info(f"Contract loaded successfully from {abi_path}")
        
        _initialized = True
        logger.info("Web3 initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Web3: {e}", exc_info=True)
        raise
    
    return w3, contract

def get_contract():
    """Get the initialized contract instance"""
    global contract
    if contract is None or not _initialized:
        init_web3()
    return contract

def get_w3():
    """Get the initialized Web3 instance"""
    global w3
    if w3 is None or not _initialized:
        init_web3()
    return w3

def is_connected():
    """Check if Web3 is connected to the network"""
    try:
        w3_instance = get_w3()
        return w3_instance.is_connected()
    except:
        return False

def get_network_info():
    """Get network information"""
    try:
        w3_instance = get_w3()
        info = {
            "chain_id": None,
            "block_number": None,
            "gas_price": None,
            "is_connected": w3_instance.is_connected(),
            "rpc_url": settings.POLYGON_RPC_URL
        }
        try:
            info["chain_id"] = w3_instance.eth.chain_id
        except Exception:
            pass
        try:
            info["block_number"] = w3_instance.eth.block_number
        except Exception:
            pass
        try:
            info["gas_price"] = w3_instance.eth.gas_price
        except Exception:
            pass
        return info
    except Exception as e:
        logger.error(f"Failed to get network info: {e}")
        return {"error": str(e), "is_connected": False}

