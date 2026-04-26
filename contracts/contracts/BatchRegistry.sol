// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title BatchRegistry
 * @dev Registry for H2 production batches with compliance verification
 */
contract BatchRegistry is Ownable {

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
    
    // State variables
    uint256 private _batchCounter;
    mapping(bytes32 => Batch) public batches;
    mapping(bytes32 => ComplianceData) public complianceData;
    mapping(address => bool) public authorizedVerifiers;
    
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
    uint256 public constant GHG_LIMIT = 3400; // 3.4 kgCO2e/kgH2 * 1000
    uint256 public constant WATER_LIMIT = 15000; // 15 liters/kgH2 * 1000
    
    // Modifiers
    modifier onlyAuthorizedVerifier() {
        require(authorizedVerifiers[msg.sender], "Not authorized verifier");
        _;
    }
    
    modifier batchExists(bytes32 batchId) {
        require(batches[batchId].timestamp > 0, "Batch does not exist");
        _;
    }
    
    constructor() Ownable(msg.sender) {
        // Owner is automatically an authorized verifier
        authorizedVerifiers[msg.sender] = true;
    }
    
    /**
     * @dev Register a new H2 production batch
     * @param batchId Unique batch identifier
     * @param sizeKg Batch size in kilograms
     * @param ghgEmissions GHG emissions (kgCO2e/kgH2 * 1000)
     * @param waterConsumption Water consumption (liters/kgH2 * 1000)
     */
    function registerBatch(
        bytes32 batchId,
        uint256 sizeKg,
        uint256 ghgEmissions,
        uint256 waterConsumption
    ) external {
        require(batches[batchId].timestamp == 0, "Batch already registered");
        require(sizeKg > 0, "Batch size must be positive");
        require(ghgEmissions > 0, "GHG emissions must be positive");
        require(waterConsumption > 0, "Water consumption must be positive");
        
        Batch memory newBatch = Batch({
            batchId: batchId,
            producer: msg.sender,
            timestamp: block.timestamp,
            sizeKg: sizeKg,
            ghgEmissions: ghgEmissions,
            waterConsumption: waterConsumption,
            complianceHash: bytes32(0),
            isCompliant: false,
            isVerified: false,
            verifier: address(0),
            verificationTimestamp: 0
        });
        
        batches[batchId] = newBatch;
        _batchCounter++;
        emit BatchRegistered(
            batchId,
            msg.sender,
            block.timestamp,
            sizeKg,
            ghgEmissions,
            waterConsumption
        );
    }
    
    /**
     * @dev Verify batch compliance with CBAM and water limits
     * @param batchId Batch identifier to verify
     * @param proofHash Hash of compliance proof (off-chain data)
     */
    function verifyBatch(
        bytes32 batchId,
        bytes32 proofHash
    ) external onlyAuthorizedVerifier batchExists(batchId) {
        Batch storage batch = batches[batchId];
        require(!batch.isVerified, "Batch already verified");
        
        // Check compliance with limits
        bool passesGhg = batch.ghgEmissions <= GHG_LIMIT;
        bool passesWater = batch.waterConsumption <= WATER_LIMIT;
        bool isCompliant = passesGhg && passesWater;
        
        // Store compliance data
        ComplianceData memory compliance = ComplianceData({
            batchId: batchId,
            ghgLimit: GHG_LIMIT,
            waterLimit: WATER_LIMIT,
            passesGhg: passesGhg,
            passesWater: passesWater,
            proofHash: proofHash
        });
        
        complianceData[batchId] = compliance;
        
        // Update batch
        batch.complianceHash = proofHash;
        batch.isCompliant = isCompliant;
        batch.isVerified = true;
        batch.verifier = msg.sender;
        batch.verificationTimestamp = block.timestamp;
        
        emit BatchVerified(batchId, msg.sender, isCompliant, proofHash);
    }
    
    /**
     * @dev Get batch details
     * @param batchId Batch identifier
     * @return Batch details
     */
    function getBatch(bytes32 batchId) external view batchExists(batchId) returns (
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
    ) {
        Batch memory batch = batches[batchId];
        return (
            batch.batchId,
            batch.producer,
            batch.timestamp,
            batch.sizeKg,
            batch.ghgEmissions,
            batch.waterConsumption,
            batch.complianceHash,
            batch.isCompliant,
            batch.isVerified,
            batch.verifier,
            batch.verificationTimestamp
        );
    }
    
    /**
     * @dev Get compliance data for a batch
     * @param batchId Batch identifier
     * @return Compliance data
     */
    function getComplianceData(bytes32 batchId) external view batchExists(batchId) returns (
        bytes32,
        uint256,
        uint256,
        bool,
        bool,
        bytes32
    ) {
        ComplianceData memory compliance = complianceData[batchId];
        return (
            compliance.batchId,
            compliance.ghgLimit,
            compliance.waterLimit,
            compliance.passesGhg,
            compliance.passesWater,
            compliance.proofHash
        );
    }
    
    /**
     * @dev Authorize or revoke a verifier
     * @param verifier Address of verifier
     * @param authorized Whether to authorize (true) or revoke (false)
     */
    function setVerifierAuthorization(address verifier, bool authorized) external onlyOwner {
        authorizedVerifiers[verifier] = authorized;
        emit VerifierAuthorized(verifier, authorized);
    }
    
    /**
     * @dev Check if a batch is compliant
     * @param batchId Batch identifier
     * @return isCompliant Whether batch is compliant
     */
    function isBatchCompliant(bytes32 batchId) external view batchExists(batchId) returns (bool) {
        return batches[batchId].isCompliant;
    }
    
    /**
     * @dev Calculate total emissions for a batch
     * @param batchId Batch identifier
     * @return totalEmissions Total emissions in kgCO2e (with 3 decimal precision)
     */
    function calculateTotalEmissions(bytes32 batchId) external view batchExists(batchId) returns (uint256) {
        Batch memory batch = batches[batchId];
        // emissions per kg * size in kg / 1000 (for precision adjustment)
        return (batch.ghgEmissions * batch.sizeKg) / 1000;
    }
    
    /**
     * @dev Calculate total water consumption for a batch
     * @param batchId Batch identifier
     * @return totalWater Total water consumption in liters (with 3 decimal precision)
     */
    function calculateTotalWater(bytes32 batchId) external view batchExists(batchId) returns (uint256) {
        Batch memory batch = batches[batchId];
        // water per kg * size in kg / 1000 (for precision adjustment)
        return (batch.waterConsumption * batch.sizeKg) / 1000;
    }
    
    /**
     * @dev Get total number of registered batches
     * @return count Total batch count
     */
    function getTotalBatches() external view returns (uint256) {
        return _batchCounter;
    }
    
    /**
     * @dev Generate a batch ID from producer and data
     * @param producer Address of producer
     * @param dataHash Hash of batch data
     * @return batchId Generated batch ID
     */
    function generateBatchId(address producer, bytes32 dataHash) public view returns (bytes32) {
        return keccak256(abi.encodePacked(producer, dataHash, block.chainid));
    }
}