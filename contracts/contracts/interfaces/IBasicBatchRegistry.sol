// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IBasicBatchRegistry
 * @dev Basic interface for Batch Registry contract
 */
interface IBasicBatchRegistry {
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
    
    // Core functions
    function registerBatch(
        bytes32 batchId,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption,
        bytes32 complianceHash
    ) external;
    
    function verifyBatch(
        bytes32 batchId,
        bool isCompliant,
        bytes32 proofHash
    ) external;
    
    // View functions
    function getBatch(bytes32 batchId) external view returns (
        bytes32 batchIdOut,
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
    
    function isBatchRegistered(bytes32 batchId) external view returns (bool);
    function isBatchVerified(bytes32 batchId) external view returns (bool);
    function isBatchCompliant(bytes32 batchId) external view returns (bool);
    
    function getProducerBatches(address producer) external view returns (bytes32[] memory);
    function getVerifierBatches(address verifier) external view returns (bytes32[] memory);
}