// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IBatchRegistry
 * @dev Interface for Batch Registry contract
 */
interface IBatchRegistry {
    // Structs
    struct Batch {
        bytes32 batchId;
        address producer;
        uint256 timestamp;
        uint256 sizeKg;
        uint256 ghgEmissions; // kgCO2e/kgH2 * 1000 (for precision)
        uint256 waterConsumption; // liters/kgH2 * 1000 (for precision)
        bytes32 complianceHash;
        bool isCompliant;
        bool isVerified;
        address verifier;
        uint256 verificationTimestamp;
    }
    
    struct ComplianceData {
        bytes32 batchId;
        uint256 ghgLimit; // CBAM limit * 1000
        uint256 waterLimit; // Water limit * 1000
        bool passesGhg;
        bool passesWater;
        bytes32 proofHash;
    }
    
    // Events
    event BatchRegistered(
        bytes32 indexed batchId,
        address indexed producer,
        uint256 timestamp,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption
    );
    
    event BatchVerified(
        bytes32 indexed batchId,
        address indexed verifier,
        bool isCompliant,
        bytes32 complianceHash
    );
    
    event VerifierAuthorized(address indexed verifier, bool authorized);
    
    // Constants
    function GHG_LIMIT() external view returns (uint256);
    function WATER_LIMIT() external view returns (uint256);
    
    // State variables (public getters)
    function batches(bytes32 batchId) external view returns (
        bytes32 id,
        address producer,
        uint256 timestamp,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption,
        bytes32 complianceHash,
        bool isCompliant,
        bool isVerified,
        address verifier,
        uint256 verificationTimestamp
    );
    
    function complianceData(bytes32 batchId) external view returns (
        bytes32 id,
        uint256 ghgLimit,
        uint256 waterLimit,
        bool passesGhg,
        bool passesWater,
        bytes32 proofHash
    );
    
    function authorizedVerifiers(address verifier) external view returns (bool);
    
    // Functions
    function registerBatch(
        bytes32 batchId,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption
    ) external;
    
    function verifyBatch(
        bytes32 batchId,
        bytes32 proofHash
    ) external;
    
    function getBatch(bytes32 batchId) external view returns (
        bytes32,
        address,
        uint256,
        uint256,
        uint256,
        uint256,
        bytes32,
        bool,
        bool,
        address,
        uint256
    );
    
    function getComplianceData(bytes32 batchId) external view returns (
        bytes32,
        uint256,
        uint256,
        bool,
        bool,
        bytes32
    );
    
    function setVerifierAuthorization(address verifier, bool authorized) external;
    
    function isBatchCompliant(bytes32 batchId) external view returns (bool);
    
    function calculateTotalEmissions(bytes32 batchId) external view returns (uint256);
    
    function calculateTotalWater(bytes32 batchId) external view returns (uint256);
    
    function getTotalBatches() external view returns (uint256);
    
    function generateBatchId(address producer, bytes32 dataHash) external view returns (bytes32);
}