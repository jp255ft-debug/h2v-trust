// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

/**
 * @title DelegationManager
 * @dev Manages delegation of CBAM reporting responsibilities with signature verification
 */
contract DelegationManager is Ownable {
    using ECDSA for bytes32;
    using MessageHashUtils for bytes32;
    
    // Structs
    struct Delegation {
        address producer;
        address declarant;
        uint256 validFrom;
        uint256 validUntil;
        bytes32 scopeHash;
        bytes32 delegationHash;
        bool isActive;
        bool isRevoked;
        address createdBy;
        uint256 createdAt;
        uint256 revokedAt;
        string revocationReason;
    }
    
    struct DelegationRequest {
        address producer;
        address declarant;
        uint256 validUntil;
        bytes32 scopeHash;
        bytes producerSignature;
        bytes declarantSignature;
    }
    
    struct Scope {
        bytes32 scopeId;
        string name;
        string description;
        bool isActive;
    }
    
    // State variables
    mapping(bytes32 => Delegation) public delegations;
    mapping(bytes32 => Scope) public scopes;
    mapping(address => bytes32[]) public producerDelegations;
    mapping(address => bytes32[]) public declarantDelegations;
    mapping(address => bool) public authorizedRegistrars;
    
    // Events
    event DelegationCreated(
        bytes32 indexed delegationId,
        address indexed producer,
        address indexed declarant,
        uint256 validFrom,
        uint256 validUntil,
        bytes32 scopeHash
    );
    
    event DelegationRevoked(
        bytes32 indexed delegationId,
        address revokedBy,
        string reason,
        uint256 timestamp
    );
    
    event ScopeRegistered(
        bytes32 indexed scopeId,
        string name,
        string description
    );
    
    event RegistrarAuthorized(address indexed registrar, bool authorized);
    
    // Constants
    uint256 public constant DEFAULT_VALIDITY_DAYS = 365;
    bytes32 public constant DEFAULT_SCOPE = keccak256("CBAM_REPORTING");
    
    // Modifiers
    modifier onlyAuthorizedRegistrar() {
        require(authorizedRegistrars[msg.sender], "Not authorized registrar");
        _;
    }
    
    modifier delegationExists(bytes32 delegationId) {
        require(delegations[delegationId].createdAt > 0, "Delegation does not exist");
        _;
    }
    
    constructor() Ownable(msg.sender) {
        authorizedRegistrars[msg.sender] = true;
        
        // Register default scope
        _registerScope(
            DEFAULT_SCOPE,
            "CBAM Reporting",
            "Delegation for CBAM compliance reporting and certificate management"
        );
    }
    
    /**
     * @dev Create a new delegation with dual signatures
     * @param request Delegation request with signatures
     * @return delegationId Unique delegation identifier
     */
    function createDelegation(
        DelegationRequest calldata request
    ) external onlyAuthorizedRegistrar returns (bytes32) {
        require(request.producer != address(0), "Invalid producer address");
        require(request.declarant != address(0), "Invalid declarant address");
        require(request.producer != request.declarant, "Producer and declarant must be different");
        require(request.validUntil > block.timestamp, "Validity must be in the future");
        
        // Verify producer signature
        bytes32 producerMessageHash = _getDelegationMessageHash(
            request.producer,
            request.declarant,
            request.validUntil,
            request.scopeHash
        );
        
        address producerSigner = producerMessageHash.toEthSignedMessageHash().recover(request.producerSignature);
        require(producerSigner == request.producer, "Invalid producer signature");
        
        // Verify declarant signature
        bytes32 declarantMessageHash = _getDelegationMessageHash(
            request.declarant,
            request.producer,
            request.validUntil,
            request.scopeHash
        );
        
        address declarantSigner = declarantMessageHash.toEthSignedMessageHash().recover(request.declarantSignature);
        require(declarantSigner == request.declarant, "Invalid declarant signature");
        
        // Generate delegation ID
        bytes32 delegationId = keccak256(
            abi.encodePacked(
                request.producer,
                request.declarant,
                request.validUntil,
                request.scopeHash,
                block.timestamp,
                block.chainid
            )
        );
        
        // Create delegation
        Delegation memory newDelegation = Delegation({
            producer: request.producer,
            declarant: request.declarant,
            validFrom: block.timestamp,
            validUntil: request.validUntil,
            scopeHash: request.scopeHash,
            delegationHash: keccak256(
                abi.encodePacked(
                    request.producer,
                    request.declarant,
                    request.validUntil,
                    request.scopeHash
                )
            ),
            isActive: true,
            isRevoked: false,
            createdBy: msg.sender,
            createdAt: block.timestamp,
            revokedAt: 0,
            revocationReason: ""
        });
        
        delegations[delegationId] = newDelegation;
        
        // Update mappings
        producerDelegations[request.producer].push(delegationId);
        declarantDelegations[request.declarant].push(delegationId);
        
        emit DelegationCreated(
            delegationId,
            request.producer,
            request.declarant,
            block.timestamp,
            request.validUntil,
            request.scopeHash
        );
        
        return delegationId;
    }
    
    /**
     * @dev Create delegation with single signature (simplified for producers)
     * @param declarant Address of declarant
     * @param validUntil Delegation validity end timestamp
     * @param scopeHash Hash of delegation scope
     * @return delegationId Unique delegation identifier
     */
    function createSimpleDelegation(
        address declarant,
        uint256 validUntil,
        bytes32 scopeHash
    ) external returns (bytes32) {
        require(declarant != address(0), "Invalid declarant address");
        require(msg.sender != declarant, "Producer and declarant must be different");
        require(validUntil > block.timestamp, "Validity must be in the future");
        
        // Use default scope if not specified
        if (scopeHash == bytes32(0)) {
            scopeHash = DEFAULT_SCOPE;
        }
        
        // Generate delegation ID
        bytes32 delegationId = keccak256(
            abi.encodePacked(
                msg.sender,
                declarant,
                validUntil,
                scopeHash,
                block.timestamp,
                block.chainid
            )
        );
        
        // Create delegation
        Delegation memory newDelegation = Delegation({
            producer: msg.sender,
            declarant: declarant,
            validFrom: block.timestamp,
            validUntil: validUntil,
            scopeHash: scopeHash,
            delegationHash: keccak256(
                abi.encodePacked(
                    msg.sender,
                    declarant,
                    validUntil,
                    scopeHash
                )
            ),
            isActive: true,
            isRevoked: false,
            createdBy: msg.sender,
            createdAt: block.timestamp,
            revokedAt: 0,
            revocationReason: ""
        });
        
        delegations[delegationId] = newDelegation;
        
        // Update mappings
        producerDelegations[msg.sender].push(delegationId);
        declarantDelegations[declarant].push(delegationId);
        
        emit DelegationCreated(
            delegationId,
            msg.sender,
            declarant,
            block.timestamp,
            validUntil,
            scopeHash
        );
        
        return delegationId;
    }
    
    /**
     * @dev Revoke a delegation
     * @param delegationId Delegation identifier
     * @param reason Reason for revocation
     */
    function revokeDelegation(
        bytes32 delegationId,
        string calldata reason
    ) external delegationExists(delegationId) {
        Delegation storage delegation = delegations[delegationId];
        
        require(delegation.isActive, "Delegation not active");
        require(
            msg.sender == delegation.producer ||
            msg.sender == delegation.declarant ||
            msg.sender == owner(),
            "Not authorized to revoke"
        );
        
        delegation.isActive = false;
        delegation.isRevoked = true;
        delegation.revokedAt = block.timestamp;
        delegation.revocationReason = reason;
        
        emit DelegationRevoked(delegationId, msg.sender, reason, block.timestamp);
    }
    
    /**
     * @dev Check if delegation is valid
     * @param delegationId Delegation identifier
     * @return isValid Whether delegation is valid
     */
    function isValidDelegation(bytes32 delegationId) public view returns (bool) {
        Delegation memory delegation = delegations[delegationId];
        
        if (delegation.createdAt == 0) return false;
        if (!delegation.isActive) return false;
        if (delegation.isRevoked) return false;
        if (block.timestamp < delegation.validFrom) return false;
        if (block.timestamp > delegation.validUntil) return false;
        
        return true;
    }
    
    /**
     * @dev Verify delegation authorization for a specific action
     * @param delegationId Delegation identifier
     * @param declarant Address claiming authorization
     * @param scopeHash Required scope hash
     * @return isAuthorized Whether declarant is authorized
     */
    function verifyAuthorization(
        bytes32 delegationId,
        address declarant,
        bytes32 scopeHash
    ) external view returns (bool) {
        if (!isValidDelegation(delegationId)) {
            return false;
        }
        
        Delegation memory delegation = delegations[delegationId];
        
        // Check declarant matches
        if (delegation.declarant != declarant) {
            return false;
        }
        
        // Check scope if specified
        if (scopeHash != bytes32(0) && delegation.scopeHash != scopeHash) {
            return false;
        }
        
        return true;
    }
    
    /**
     * @dev Register a new delegation scope
     * @param scopeId Scope identifier
     * @param name Scope name
     * @param description Scope description
     */
    function registerScope(
        bytes32 scopeId,
        string calldata name,
        string calldata description
    ) external onlyOwner {
        _registerScope(scopeId, name, description);
    }
    
    /**
     * @dev Get delegation details
     * @param delegationId Delegation identifier
     * @return Delegation details
     */
    function getDelegation(bytes32 delegationId) external view delegationExists(delegationId) returns (
        address,
        address,
        uint256,
        uint256,
        bytes32,
        bytes32,
        bool,
        bool,
        address,
        uint256,
        uint256,
        string memory
    ) {
        Delegation memory delegation = delegations[delegationId];
        return (
            delegation.producer,
            delegation.declarant,
            delegation.validFrom,
            delegation.validUntil,
            delegation.scopeHash,
            delegation.delegationHash,
            delegation.isActive,
            delegation.isRevoked,
            delegation.createdBy,
            delegation.createdAt,
            delegation.revokedAt,
            delegation.revocationReason
        );
    }
    
    /**
     * @dev Get delegations for a producer
     * @param producer Address of producer
     * @return Array of delegation IDs
     */
    function getProducerDelegations(address producer) external view returns (bytes32[] memory) {
        return producerDelegations[producer];
    }
    
    /**
     * @dev Get delegations for a declarant
     * @param declarant Address of declarant
     * @return Array of delegation IDs
     */
    function getDeclarantDelegations(address declarant) external view returns (bytes32[] memory) {
        return declarantDelegations[declarant];
    }
    
    /**
     * @dev Get scope details
     * @param scopeId Scope identifier
     * @return Scope details
     */
    function getScope(bytes32 scopeId) external view returns (
        bytes32,
        string memory,
        string memory,
        bool
    ) {
        Scope memory scope = scopes[scopeId];
        require(scope.scopeId != bytes32(0), "Scope not found");
        
        return (
            scope.scopeId,
            scope.name,
            scope.description,
            scope.isActive
        );
    }
    
    /**
     * @dev Authorize or revoke a registrar
     * @param registrar Address of registrar
     * @param authorized Whether to authorize (true) or revoke (false)
     */
    function setRegistrarAuthorization(address registrar, bool authorized) external onlyOwner {
        authorizedRegistrars[registrar] = authorized;
        emit RegistrarAuthorized(registrar, authorized);
    }
    
    /**
     * @dev Generate delegation message hash for signing
     * @param signer Address of signer
     * @param counterparty Address of counterparty
     * @param validUntil Delegation validity end timestamp
     * @param scopeHash Hash of delegation scope
     * @return messageHash Hash for signing
     */
    function getDelegationMessageHash(
        address signer,
        address counterparty,
        uint256 validUntil,
        bytes32 scopeHash
    ) external pure returns (bytes32) {
        return _getDelegationMessageHash(signer, counterparty, validUntil, scopeHash);
    }
    
    // Internal functions
    
    function _registerScope(
        bytes32 scopeId,
        string memory name,
        string memory description
    ) internal {
        require(scopes[scopeId].scopeId == bytes32(0), "Scope already registered");
        
        Scope memory newScope = Scope({
            scopeId: scopeId,
            name: name,
            description: description,
            isActive: true
        });
        
        scopes[scopeId] = newScope;
        
        emit ScopeRegistered(scopeId, name, description);
    }
    
    function _getDelegationMessageHash(
        address signer,
        address counterparty,
        uint256 validUntil,
        bytes32 scopeHash
    ) internal pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(
                "\x19Ethereum Signed Message:\n32",
                keccak256(
                    abi.encodePacked(
                        signer,
                        counterparty,
                        validUntil,
                        scopeHash,
                        "DELEGATION_AUTH"
                    )
                )
            )
        );
    }
}