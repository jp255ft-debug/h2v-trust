// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IBasicComplianceVerifier
 * @dev Basic interface for Compliance Verifier contract
 */
interface IBasicComplianceVerifier {
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
    
    event ComplianceVerified(
        bytes32 indexed batchId,
        address indexed verifier,
        bool isCompliant,
        bytes32 proofHash
    );
    
    // Core functions
    function createDelegation(
        address declarant,
        uint256 validUntil
    ) external returns (bytes32);
    
    function revokeDelegation(bytes32 delegationId) external;
    
    function verifyCompliance(
        bytes32 batchId,
        uint256 ghgEmissions,
        uint256 waterConsumption,
        bytes32 proofHash
    ) external returns (bool);
    
    // View functions
    function getDelegation(bytes32 delegationId) external view returns (
        address producer,
        address declarant,
        uint256 validUntil,
        bytes32 delegationHash,
        bool isActive,
        bool isRevoked,
        uint256 revokedAt
    );
    
    function getVerificationResult(bytes32 batchId) external view returns (
        bool isCompliant,
        uint256 ghgScore,
        uint256 waterScore,
        uint256 overallScore,
        bytes32 proofHash,
        address verifier,
        uint256 timestamp
    );
    
    function calculatePenalty(
        bytes32 batchId,
        uint256 ghgEmissions,
        uint256 waterConsumption
    ) external view returns (
        uint256 excessEmissions,
        uint256 penaltyAmount,
        uint256 penaltyRate,
        bool penaltyApplicable
    );
    
    function isDelegationActive(bytes32 delegationId) external view returns (bool);
    function isAuthorizedVerifier(address verifier) external view returns (bool);
    function getProducerDelegations(address producer) external view returns (bytes32[] memory);
    function getDeclarantDelegations(address declarant) external view returns (bytes32[] memory);
}