// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title GreenHydrogenSBT
 * @dev Soulbound Token (SBT) for Green Hydrogen Certificates
 * SBTs are non-transferable tokens representing verified green hydrogen production
 */
contract GreenHydrogenSBT is ERC721, ERC721URIStorage, Ownable {

    // Structs
    struct CertificateData {
        bytes32 batchId;
        address producer;
        uint256 timestamp;
        uint256 sizeKg;
        uint256 ghgEmissions; // kgCO2e/kgH2 * 1000
        uint256 waterConsumption; // liters/kgH2 * 1000
        bool isCompliant;
        bytes32 complianceHash;
        bool isConsumed;
        uint256 consumedAt;
        address consumedBy;
    }
    
    // State variables
    uint256 private _tokenIdCounter;
    mapping(uint256 => CertificateData) public certificateData;
    mapping(bytes32 => uint256) public batchToTokenId;
    mapping(address => uint256[]) public producerCertificates;
    mapping(address => uint256[]) public ownerCertificates;
    
    // Interfaces
    address public batchRegistry;
    address public complianceVerifier;
    
    // Events
    event CertificateMinted(
        uint256 indexed tokenId,
        bytes32 indexed batchId,
        address indexed producer,
        uint256 timestamp,
        uint256 sizeKg,
        bool isCompliant
    );
    
    event CertificateConsumed(
        uint256 indexed tokenId,
        address consumedBy,
        uint256 timestamp
    );
    
    event BatchRegistryUpdated(address indexed oldRegistry, address indexed newRegistry);
    event ComplianceVerifierUpdated(address indexed oldVerifier, address indexed newVerifier);
    
    // Modifiers
    modifier onlyComplianceVerifier() {
        require(msg.sender == complianceVerifier, "Caller is not compliance verifier");
        _;
    }
    
    modifier tokenExists(uint256 tokenId) {
        require(_ownerOf(tokenId) != address(0), "Token does not exist");
        _;
    }
    
    modifier notConsumed(uint256 tokenId) {
        require(!certificateData[tokenId].isConsumed, "Certificate already consumed");
        _;
    }
    
    constructor(
        string memory name,
        string memory symbol,
        address _batchRegistry,
        address _complianceVerifier
    ) ERC721(name, symbol) Ownable(msg.sender) {
        require(_batchRegistry != address(0), "Invalid batch registry address");
        require(_complianceVerifier != address(0), "Invalid compliance verifier address");
        
        batchRegistry = _batchRegistry;
        complianceVerifier = _complianceVerifier;
    }
    
    /**
     * @dev Mint a new SBT certificate for a verified batch
     * @param batchId Batch identifier
     * @param producer Address of hydrogen producer
     * @param _tokenURI URI for certificate metadata
     * @return tokenId Minted token ID
     */
    function mintCertificate(
        bytes32 batchId,
        address producer,
        string memory _tokenURI
    ) external onlyOwner returns (uint256) {
        require(batchToTokenId[batchId] == 0, "Certificate already minted for this batch");
        require(producer != address(0), "Invalid producer address");
        
        // Get batch data from registry (simplified - in production would call registry)
        // For MVP, we assume batch is verified and compliant
        
        // Mint token
        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;
        
        _safeMint(producer, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        
        // Store certificate data (simplified for MVP)
        CertificateData memory data = CertificateData({
            batchId: batchId,
            producer: producer,
            timestamp: block.timestamp,
            sizeKg: 1000, // Default for MVP
            ghgEmissions: 2500, // 2.5 kgCO2e/kgH2 * 1000 (compliant)
            waterConsumption: 12000, // 12 liters/kgH2 * 1000 (compliant)
            isCompliant: true,
            complianceHash: keccak256(abi.encodePacked(batchId, block.timestamp)),
            isConsumed: false,
            consumedAt: 0,
            consumedBy: address(0)
        });
        
        certificateData[tokenId] = data;
        batchToTokenId[batchId] = tokenId;
        producerCertificates[producer].push(tokenId);
        ownerCertificates[producer].push(tokenId);
        
        emit CertificateMinted(tokenId, batchId, producer, block.timestamp, data.sizeKg, data.isCompliant);
        
        return tokenId;
    }
    
    /**
     * @dev Consume a certificate (mark as used for carbon accounting)
     * @param tokenId Token ID to consume
     */
    function consumeCertificate(uint256 tokenId) external tokenExists(tokenId) notConsumed(tokenId) {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        
        CertificateData storage data = certificateData[tokenId];
        data.isConsumed = true;
        data.consumedAt = block.timestamp;
        data.consumedBy = msg.sender;
        
        emit CertificateConsumed(tokenId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Get certificate data
     * @param tokenId Token ID
     * @return Certificate data
     */
    function getCertificateData(uint256 tokenId) external view tokenExists(tokenId) returns (
        bytes32,
        address,
        uint256,
        uint256,
        uint256,
        uint256,
        bool,
        bytes32,
        bool,
        uint256,
        address
    ) {
        CertificateData memory data = certificateData[tokenId];
        return (
            data.batchId,
            data.producer,
            data.timestamp,
            data.sizeKg,
            data.ghgEmissions,
            data.waterConsumption,
            data.isCompliant,
            data.complianceHash,
            data.isConsumed,
            data.consumedAt,
            data.consumedBy
        );
    }
    
    /**
     * @dev Get token ID for a batch
     * @param batchId Batch identifier
     * @return tokenId Token ID (0 if not minted)
     */
    function getTokenIdForBatch(bytes32 batchId) external view returns (uint256) {
        return batchToTokenId[batchId];
    }
    
    /**
     * @dev Get certificates for a producer
     * @param producer Producer address
     * @return Array of token IDs
     */
    function getProducerCertificates(address producer) external view returns (uint256[] memory) {
        return producerCertificates[producer];
    }
    
    /**
     * @dev Get certificates owned by an address
     * @param owner Owner address
     * @return Array of token IDs
     */
    function getOwnerCertificates(address owner) external view returns (uint256[] memory) {
        return ownerCertificates[owner];
    }
    
    /**
     * @dev Check if certificate is valid (not consumed and compliant)
     * @param tokenId Token ID
     * @return isValid Whether certificate is valid
     */
    function isValidCertificate(uint256 tokenId) external view tokenExists(tokenId) returns (bool) {
        CertificateData memory data = certificateData[tokenId];
        return !data.isConsumed && data.isCompliant;
    }
    
    /**
     * @dev Calculate carbon savings for a certificate
     * @param tokenId Token ID
     * @return savingsKg CO2 savings in kg compared to grey hydrogen
     */
    function calculateCarbonSavings(uint256 tokenId) external view tokenExists(tokenId) returns (uint256) {
        CertificateData memory data = certificateData[tokenId];
        
        // Grey hydrogen emissions: ~10 kgCO2e/kgH2
        uint256 greyHydrogenEmissions = 10000; // 10 kgCO2e/kgH2 * 1000
        
        // Calculate savings
        uint256 savingsPerKg = greyHydrogenEmissions - data.ghgEmissions;
        uint256 totalSavings = (savingsPerKg * data.sizeKg) / 1000;
        
        return totalSavings;
    }
    
    /**
     * @dev Update batch registry address
     * @param newRegistry New batch registry address
     */
    function updateBatchRegistry(address newRegistry) external onlyOwner {
        require(newRegistry != address(0), "Invalid registry address");
        
        address oldRegistry = batchRegistry;
        batchRegistry = newRegistry;
        
        emit BatchRegistryUpdated(oldRegistry, newRegistry);
    }
    
    /**
     * @dev Update compliance verifier address
     * @param newVerifier New compliance verifier address
     */
    function updateComplianceVerifier(address newVerifier) external onlyOwner {
        require(newVerifier != address(0), "Invalid verifier address");
        
        address oldVerifier = complianceVerifier;
        complianceVerifier = newVerifier;
        
        emit ComplianceVerifierUpdated(oldVerifier, newVerifier);
    }
    
    /**
     * @dev Get total certificates minted
     * @return count Total certificate count
     */
    function getTotalCertificates() external view returns (uint256) {
        return _tokenIdCounter;
    }
    
    // Override transfer functions to make token soulbound (non-transferable)
    
    /**
     * @dev Override transferFrom to prevent transfers (Soulbound Token)
     */
    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public virtual override(ERC721, IERC721) {
        // Only allow transfers if initiated by owner (for special cases like migration)
        if (msg.sender != owner()) {
            revert("SBT: Token is non-transferable");
        }
        
        super.transferFrom(from, to, tokenId);
        
        // Update owner certificates mapping
        if (from != address(0)) {
            _removeFromArray(ownerCertificates[from], tokenId);
        }
        if (to != address(0)) {
            ownerCertificates[to].push(tokenId);
        }
    }
    
    /**
     * @dev Override safeTransferFrom to prevent transfers (Soulbound Token)
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) public virtual override(ERC721, IERC721) {
        // Only allow transfers if initiated by owner (for special cases like migration)
        if (msg.sender != owner()) {
            revert("SBT: Token is non-transferable");
        }
        
        super.safeTransferFrom(from, to, tokenId, data);
        
        // Update owner certificates mapping
        if (from != address(0)) {
            _removeFromArray(ownerCertificates[from], tokenId);
        }
        if (to != address(0)) {
            ownerCertificates[to].push(tokenId);
        }
    }
    
    // The following functions are overrides required by Solidity
    
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    // Internal functions
    
    function _removeFromArray(uint256[] storage array, uint256 value) internal {
        for (uint256 i = 0; i < array.length; i++) {
            if (array[i] == value) {
                array[i] = array[array.length - 1];
                array.pop();
                break;
            }
        }
    }
    
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721)
        returns (address)
    {
        // Prevent transfers except for minting and burning
        if (auth != address(0) && auth != owner()) {
            revert("SBT: Token is non-transferable");
        }
        
        return super._update(to, tokenId, auth);
    }
}