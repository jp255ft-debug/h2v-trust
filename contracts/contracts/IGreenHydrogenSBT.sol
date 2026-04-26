// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IGreenHydrogenSBT
 * @dev Interface for Green Hydrogen Soulbound Token (SBT) contract
 */
interface IGreenHydrogenSBT {
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
    
    // State variables (public getters)
    function certificateData(uint256 tokenId) external view returns (
        bytes32 batchId,
        address producer,
        uint256 timestamp,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption,
        bool isCompliant,
        bytes32 complianceHash,
        bool isConsumed,
        uint256 consumedAt,
        address consumedBy
    );
    
    function batchToTokenId(bytes32 batchId) external view returns (uint256);
    function batchRegistry() external view returns (address);
    function complianceVerifier() external view returns (address);
    
    // Functions
    function mintCertificate(
        bytes32 batchId,
        address producer,
        string memory _tokenURI
    ) external returns (uint256);
    
    function consumeCertificate(uint256 tokenId) external;
    
    function getCertificateData(uint256 tokenId) external view returns (
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
    );
    
    function getTokenIdForBatch(bytes32 batchId) external view returns (uint256);
    
    function getProducerCertificates(address producer) external view returns (uint256[] memory);
    
    function getOwnerCertificates(address owner) external view returns (uint256[] memory);
    
    function isValidCertificate(uint256 tokenId) external view returns (bool);
    
    function calculateCarbonSavings(uint256 tokenId) external view returns (uint256);
    
    function updateBatchRegistry(address newRegistry) external;
    
    function updateComplianceVerifier(address newVerifier) external;
    
    function getTotalCertificates() external view returns (uint256);
    
    // ERC721 functions (inherited)
    function ownerOf(uint256 tokenId) external view returns (address);
    function tokenURI(uint256 tokenId) external view returns (string memory);
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}