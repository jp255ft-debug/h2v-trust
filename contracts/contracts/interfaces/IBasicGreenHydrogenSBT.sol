// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IBasicGreenHydrogenSBT
 * @dev Basic interface for Green Hydrogen Soulbound Token (SBT) contract
 */
interface IBasicGreenHydrogenSBT {
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
    
    // Core functions
    function mintCertificate(
        bytes32 batchId,
        address producer,
        string memory _tokenURI
    ) external returns (uint256);
    
    function consumeCertificate(uint256 tokenId) external;
    
    // View functions
    function ownerOf(uint256 tokenId) external view returns (address);
    function tokenURI(uint256 tokenId) external view returns (string memory);
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
    
    function getCertificateData(uint256 tokenId) external view returns (
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
    
    function getTokenIdForBatch(bytes32 batchId) external view returns (uint256);
    function isValidCertificate(uint256 tokenId) external view returns (bool);
}