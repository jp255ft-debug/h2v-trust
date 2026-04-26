// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IComplianceVerifier
 * @dev Interface for Compliance Verifier contract
 */
interface IComplianceVerifier {
    // Structs
    struct Delegation {
        address producer;
        address declarant;
        uint256 validUntil;
        bytes32 delegationHash;
        bool isActive;
        bool isRevoked;
        uint256 revokedAt;
    }
    
    struct VerificationResult {
        bytes32 batchId;
        bool isCompliant;
        uint256 ghgScore; // 0-1000 (higher is better)
        uint256 waterScore; // 0-1000 (higher is better)
        uint256 overallScore; // 0-1000 (higher is better)
        bytes32 proofHash;
        address verifier;
        uint256 timestamp;
    }
    
    struct PenaltyCalculation {
        bytes32 batchId;
        uint256 excessEmissions; // kgCO2e * 1000
        uint256 penaltyAmount; // EUR * 1000
        uint256 penaltyRate; // EUR per ton CO2 * 1000
        bool penaltyApplicable;
    }
    
    // Events
    event DelegationCreated(
        bytes32 indexed delegationId,
        address indexed producer,
        address indexed declarant,
        uint256 validUntil
    );
    
    event DelegationRevoked(
        bytes32 indexed delegationId,
        address revokedBy,
        uint256 timestamp
    );
    
    event BatchVerified(
        bytes32 indexed batchId,
        address indexed verifier,
        bool isCompliant,
        uint256 overallScore,
        bytes32 proofHash
    );
    
    event PenaltyCalculated(
        bytes32 indexed batchId,
        uint256 excessEmissions,
        uint256 penaltyAmount,
        bool penaltyApplicable
    );
    
    event AuditorAuthorized(address indexed auditor, bool authorized);
    
    // Constants
    function MAX_GHG_SCORE() external view returns (uint256);
    function MAX_WATER_SCORE() external view returns (uint256);
    function PENALTY_RATE() external view returns (uint256);
    function DELEGATION_VALIDITY_DAYS() external view returns (uint256);
    
    // State variables (public getters)
    function batchRegistry() external view returns (address);
    function delegations(bytes32 delegationId) external view returns (
        address producer,
        address declarant,
        uint256 validUntil,
        bytes32 delegationHash,
        bool isActive,
        bool isRevoked,
        uint256 revokedAt
    );
    
    function verificationResults(bytes32 batchId) external view returns (
        bytes32 id,
        bool isCompliant,
        uint256 ghgScore,
        uint256 waterScore,
        uint256 overallScore,
        bytes32 proofHash,
        address verifier,
        uint256 timestamp
    );
    
    function penaltyCalculations(bytes32 batchId) external view returns (
        bytes32 id,
        uint256 excessEmissions,
        uint256 penaltyAmount,
        uint256 penaltyRate,
        bool penaltyApplicable
    );
    
    function authorizedAuditors(address auditor) external view returns (bool);
    
    // Functions
    function createDelegation(
        address producer,
        address declarant
    ) external returns (bytes32);
    
    function revokeDelegation(bytes32 delegationId) external;
    
    function verifyBatchCompliance(
        bytes32 batchId,
        bytes32 proofHash,
        bytes32 delegationId
    ) external;
    
    function calculateGhgScore(uint256 ghgEmissions) external pure returns (uint256);
    
    function calculateWaterScore(uint256 waterConsumption) external pure returns (uint256);
    
    function validDelegationCheck(bytes32 delegationId) external view returns (bool);
    
    function getVerificationResult(bytes32 batchId) external view returns (
        bytes32,
        bool,
        uint256,
        uint256,
        uint256,
        bytes32,
        address,
        uint256
    );
    
    function getPenaltyCalculation(bytes32 batchId) external view returns (
        bytes32,
        uint256,
        uint256,
        uint256,
        bool
    );
    
    function setAuditorAuthorization(address auditor, bool authorized) external;
    
    function isAuthorizedForBatch(bytes32 batchId, address verifier) external view returns (bool);
}