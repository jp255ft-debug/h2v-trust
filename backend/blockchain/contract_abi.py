"""
Contract ABIs for blockchain interaction.
Contains the ABI definitions for GreenHydrogenSBT and related contracts.
"""

# GreenHydrogenSBT Contract ABI
GREEN_HYDROGEN_SBT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "string", "name": "uri", "type": "string"},
        ],
        "name": "safeMint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "isConsumed",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "consume",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
            {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"},
        ],
        "name": "CertificateConsumed",
        "type": "event",
    },
]

# BatchRegistry Contract ABI
BATCH_REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "batchHash", "type": "string"},
            {"internalType": "address", "name": "producer", "type": "address"},
        ],
        "name": "registerBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "batchId", "type": "string"}],
        "name": "getBatch",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bool", "name": "", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "batchId", "type": "string"}],
        "name": "isBatchRegistered",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# ComplianceVerifier Contract ABI
COMPLIANCE_VERIFIER_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "uint256", "name": "ghgEmissions", "type": "uint256"},
            {"internalType": "uint256", "name": "waterConsumption", "type": "uint256"},
        ],
        "name": "verifyCompliance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "batchId", "type": "string"}],
        "name": "getComplianceStatus",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# DelegationManager Contract ABI
DELEGATION_MANAGER_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "declarant", "type": "address"},
            {"internalType": "uint256", "name": "validUntil", "type": "uint256"},
        ],
        "name": "authorizeDelegation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "revokeDelegation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "producer", "type": "address"}],
        "name": "getDelegation",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bool", "name": "", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# Contract address mapping
CONTRACT_ADDRESSES = {
    "GreenHydrogenSBT": "0x0000000000000000000000000000000000000000",  # To be updated after deployment
    "BatchRegistry": "0x0000000000000000000000000000000000000000",
    "ComplianceVerifier": "0x0000000000000000000000000000000000000000",
    "DelegationManager": "0x0000000000000000000000000000000000000000",
}

# Contract name to ABI mapping
CONTRACT_ABIS = {
    "GreenHydrogenSBT": GREEN_HYDROGEN_SBT_ABI,
    "BatchRegistry": BATCH_REGISTRY_ABI,
    "ComplianceVerifier": COMPLIANCE_VERIFIER_ABI,
    "DelegationManager": DELEGATION_MANAGER_ABI,
}


def get_contract_abi(contract_name: str) -> list:
    """Get ABI for a specific contract by name."""
    return CONTRACT_ABIS.get(contract_name, [])


def get_contract_address(contract_name: str) -> str:
    """Get deployed address for a specific contract."""
    return CONTRACT_ADDRESSES.get(contract_name, "")


def update_contract_address(contract_name: str, address: str):
    """Update the deployed address for a contract after deployment."""
    if contract_name in CONTRACT_ADDRESSES:
        CONTRACT_ADDRESSES[contract_name] = address
