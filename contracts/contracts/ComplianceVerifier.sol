// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./BatchRegistry.sol";

/**
 * @title ComplianceVerifier
 * @dev Advanced compliance verification with delegation support for CBAM reporting
 */
contract ComplianceVerifier is Ownable {
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
    
    // State variables
    BatchRegistry public batchRegistry;
    mapping(bytes32 => Delegation) public delegations;
    mapping(bytes32 => VerificationResult) public verificationResults;
    mapping(bytes32 => PenaltyCalculation) public penaltyCalculations;
    mapping(address => bool) public authorizedAuditors;
    
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
    uint256 public constant MAX_GHG_SCORE = 1000;
    uint256 public constant MAX_WATER_SCORE = 1000;
    uint256 public constant PENALTY_RATE = 50000; // 50 EUR/ton CO2 * 1000
    uint256 public constant DELEGATION_VALIDITY_DAYS = 365;
    
    // Modifiers
    modifier onlyAuthorizedAuditor() {
        require(authorizedAuditors[msg.sender], "Not authorized auditor");
        _;
    }
    
    modifier validDelegation(bytes32 delegationId) {
        require(delegations[delegationId].isActive, "Delegation not active");
        require(!delegations[delegationId].isRevoked, "Delegation revoked");
        require(delegations[delegationId].validUntil > block.timestamp, "Delegation expired");
        _;
    }
    
    constructor(address _batchRegistry) Ownable(msg.sender) {
        require(_batchRegistry != address(0), "Invalid batch registry address");
        batchRegistry = BatchRegistry(_batchRegistry);
        authorizedAuditors[msg.sender] = true;
    }
    
    /**
     * @dev Create a delegation for CBAM reporting
     * @param producer Address of hydrogen producer
     * @param declarant Address of CBAM declarant
     * @return delegationId Unique delegation identifier
     */
    function createDelegation(
        address producer,
        address declarant
    ) external returns (bytes32) {
        require(producer != address(0), "Invalid producer address");
        require(declarant != address(0), "Invalid declarant address");
        require(producer == msg.sender, "Only producer can create delegation");
        
        bytes32 delegationId = keccak256(
            abi.encodePacked(producer, declarant, block.timestamp, block.chainid)
        );
        
        uint256 validUntil = block.timestamp + (DELEGATION_VALIDITY_DAYS * 1 days);
        
        Delegation memory newDelegation = Delegation({
            producer: producer,
            declarant: declarant,
            validUntil: validUntil,
            delegationHash: keccak256(
                abi.encodePacked(producer, declarant, validUntil)
            ),
            isActive: true,
            isRevoked: false,
            revokedAt: 0
        });
        
        delegations[delegationId] = newDelegation;
        
        emit DelegationCreated(delegationId, producer, declarant, validUntil);
        
        return delegationId;
    }
    
    /**
     * @dev Revoke a delegation
     * @param delegationId Delegation identifier
     */
    function revokeDelegation(bytes32 delegationId) external {
        Delegation storage delegation = delegations[delegationId];
        require(delegation.isActive, "Delegation not active");
        require(
            msg.sender == delegation.producer || msg.sender == owner(),
            "Not authorized to revoke"
        );
        
        delegation.isActive = false;
        delegation.isRevoked = true;
        delegation.revokedAt = block.timestamp;
        
        emit DelegationRevoked(delegationId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Verify batch compliance with detailed scoring
     * @param batchId Batch identifier
     * @param proofHash Hash of compliance proof
     * @param delegationId Optional delegation ID for authorized verification
     */
    function verifyBatchCompliance(
        bytes32 batchId,
        bytes32 proofHash,
        bytes32 delegationId
    ) external onlyAuthorizedAuditor {
        // Check if batch exists in registry
        (bytes32 returnedBatchId,,,,,,,,,,) = batchRegistry.getBatch(batchId);
        require(returnedBatchId != bytes32(0), "Batch not found in registry");
        
        // Check delegation if provided
        if (delegationId != bytes32(0)) {
            require(
                delegations[delegationId].declarant == msg.sender,
                "Not authorized by delegation"
            );
            require(
                validDelegationCheck(delegationId),
                "Invalid delegation"
            );
        }
        
        // Get batch data
        (,,,, uint256 ghgEmissions, uint256 waterConsumption,, bool isCompliant,,,) = batchRegistry.getBatch(batchId);
        
        // Calculate detailed scores
        uint256 ghgScore = calculateGhgScore(ghgEmissions);
        uint256 waterScore = calculateWaterScore(waterConsumption);
        uint256 overallScore = (ghgScore * 6 + waterScore * 4) / 10; // Weighted average
        
        // Store verification result
        VerificationResult memory result = VerificationResult({
            batchId: batchId,
            isCompliant: isCompliant,
            ghgScore: ghgScore,
            waterScore: waterScore,
            overallScore: overallScore,
            proofHash: proofHash,
            verifier: msg.sender,
            timestamp: block.timestamp
        });
        
        verificationResults[batchId] = result;
        
        // Calculate penalty if applicable
        if (!isCompliant) {
            calculatePenalty(batchId, ghgEmissions);
        }
        
        emit BatchVerified(batchId, msg.sender, isCompliant, overallScore, proofHash);
    }
    
    /**
     * @dev Calculate GHG compliance score (0-1000)
     * @param ghgEmissions GHG emissions (kgCO2e/kgH2 * 1000)
     * @return score GHG compliance score
     */
    function calculateGhgScore(uint256 ghgEmissions) public pure returns (uint256) {
        uint256 ghgLimit = 3400; // 3.4 kgCO2e/kgH2 * 1000
        
        if (ghgEmissions <= ghgLimit) {
            return MAX_GHG_SCORE;
        }
        
        // Linear decrease from limit to 2x limit
        uint256 maxExcess = ghgLimit; // Allow up to 2x limit
        uint256 excess = ghgEmissions - ghgLimit;
        
        if (excess >= maxExcess) {
            return 0;
        }
        
        // Score decreases linearly with excess emissions
        return MAX_GHG_SCORE - ((excess * MAX_GHG_SCORE) / maxExcess);
    }
    
    /**
     * @dev Calculate water compliance score (0-1000)
     * @param waterConsumption Water consumption (liters/kgH2 * 1000)
     * @return score Water compliance score
     */
    function calculateWaterScore(uint256 waterConsumption) public pure returns (uint256) {
        uint256 waterLimit = 15000; // 15 liters/kgH2 * 1000
        
        if (waterConsumption <= waterLimit) {
            return MAX_WATER_SCORE;
        }
        
        // Linear decrease from limit to 2x limit
        uint256 maxExcess = waterLimit; // Allow up to 2x limit
        uint256 excess = waterConsumption - waterLimit;
        
        if (excess >= maxExcess) {
            return 0;
        }
        
        // Score decreases linearly with excess consumption
        return MAX_WATER_SCORE - ((excess * MAX_WATER_SCORE) / maxExcess);
    }
    
    /**
     * @dev Calculate CBAM penalty for non-compliant batch
     * @param batchId Batch identifier
     * @param ghgEmissions GHG emissions (kgCO2e/kgH2 * 1000)
     */
    function calculatePenalty(bytes32 batchId, uint256 ghgEmissions) internal {
        uint256 ghgLimit = 3400; // 3.4 kgCO2e/kgH2 * 1000
        
        if (ghgEmissions <= ghgLimit) {
            // No penalty
            PenaltyCalculation memory noPenalty = PenaltyCalculation({
                batchId: batchId,
                excessEmissions: 0,
                penaltyAmount: 0,
                penaltyRate: PENALTY_RATE,
                penaltyApplicable: false
            });
            
            penaltyCalculations[batchId] = noPenalty;
            return;
        }
        
        // Get batch size
        (,,,, uint256 sizeKg,,,,,,) = batchRegistry.getBatch(batchId);
        
        // Calculate excess emissions (kgCO2e * 1000)
        uint256 excessPerKg = ghgEmissions - ghgLimit;
        uint256 totalExcess = (excessPerKg * sizeKg) / 1000; // Convert to kgCO2e
        
        // Calculate penalty (EUR * 1000)
        // penalty = (excess in tons) * (rate in EUR/ton)
        // excess in tons = totalExcess / 1,000,000 (since totalExcess is kg * 1000)
        uint256 penaltyAmount = (totalExcess * PENALTY_RATE) / 1_000_000_000;
        
        PenaltyCalculation memory penalty = PenaltyCalculation({
            batchId: batchId,
            excessEmissions: totalExcess,
            penaltyAmount: penaltyAmount,
            penaltyRate: PENALTY_RATE,
            penaltyApplicable: true
        });
        
        penaltyCalculations[batchId] = penalty;
        
        emit PenaltyCalculated(batchId, totalExcess, penaltyAmount, true);
    }
    
    /**
     * @dev Check if delegation is valid
     * @param delegationId Delegation identifier
     * @return isValid Whether delegation is valid
     */
    function validDelegationCheck(bytes32 delegationId) public view returns (bool) {
        Delegation memory delegation = delegations[delegationId];
        
        return delegation.isActive &&
               !delegation.isRevoked &&
               delegation.validUntil > block.timestamp;
    }
    
    /**
     * @dev Get verification result for a batch
     * @param batchId Batch identifier
     * @return Verification result
     */
    function getVerificationResult(bytes32 batchId) external view returns (
        bytes32,
        bool,
        uint256,
        uint256,
        uint256,
        bytes32,
        address,
        uint256
    ) {
        VerificationResult memory result = verificationResults[batchId];
        return (
            result.batchId,
            result.isCompliant,
            result.ghgScore,
            result.waterScore,
            result.overallScore,
            result.proofHash,
            result.verifier,
            result.timestamp
        );
    }
    
    /**
     * @dev Get penalty calculation for a batch
     * @param batchId Batch identifier
     * @return Penalty calculation
     */
    function getPenaltyCalculation(bytes32 batchId) external view returns (
        bytes32,
        uint256,
        uint256,
        uint256,
        bool
    ) {
        PenaltyCalculation memory penalty = penaltyCalculations[batchId];
        return (
            penalty.batchId,
            penalty.excessEmissions,
            penalty.penaltyAmount,
            penalty.penaltyRate,
            penalty.penaltyApplicable
        );
    }
    
    /**
     * @dev Authorize or revoke an auditor
     * @param auditor Address of auditor
     * @param authorized Whether to authorize (true) or revoke (false)
     */
    function setAuditorAuthorization(address auditor, bool authorized) external onlyOwner {
        authorizedAuditors[auditor] = authorized;
        emit AuditorAuthorized(auditor, authorized);
    }
    
    /**
     * @dev Check if address is authorized to verify a specific batch
     * @param batchId Batch identifier
     * @param verifier Address to check
     * @return isAuthorized Whether address is authorized
     */
    function isAuthorizedForBatch(bytes32 batchId, address verifier) external view returns (bool) {
        // Check if verifier is an authorized auditor
        if (!authorizedAuditors[verifier]) {
            return false;
        }
        
        // Check if batch exists
        (bytes32 returnedBatchId, address producer,,,,,,,,,) = batchRegistry.getBatch(batchId);
        if (returnedBatchId == bytes32(0)) {
            return false;
        }
        
        // Check if verifier has delegation from producer
        bytes32 delegationId = keccak256(
            abi.encodePacked(producer, verifier, block.timestamp, block.chainid)
        );
        
        // Try to find delegation (simplified check)
        // In production, would need to iterate or use mapping
        return validDelegationCheck(delegationId);
    }
}