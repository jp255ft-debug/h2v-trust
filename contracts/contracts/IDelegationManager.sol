// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title IDelegationManager
 * @dev Interface for Delegation Manager contract
 */
interface IDelegationManager {
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
    function DEFAULT_VALIDITY_DAYS() external view returns (uint256);
    function DEFAULT_SCOPE() external view returns (bytes32);
    
    // State variables (public getters)
    function delegations(bytes32 delegationId) external view returns (
        address producer,
        address declarant,
        uint256 validFrom,
        uint256 validUntil,
        bytes32 scopeHash,
        bytes32 delegationHash,
        bool isActive,
        bool isRevoked,
        address createdBy,
        uint256 createdAt,
        uint256 revokedAt,
        string memory revocationReason
    );
    
    function scopes(bytes32 scopeId) external view returns (
        bytes32 id,
        string memory name,
        string memory description,
        bool isActive
    );
    
    function producerDelegations(address producer) external view returns (bytes32[] memory);
    function declarantDelegations(address declarant) external view returns (bytes32[] memory);
    function authorizedRegistrars(address registrar) external view returns (bool);
    
    // Functions
    function createDelegation(
        DelegationRequest calldata request
    ) external returns (bytes32);
    
    function createSimpleDelegation(
        address declarant,
        uint256 validUntil,
        bytes32 scopeHash
    ) external returns (bytes32);
    
    function revokeDelegation(
        bytes32 delegationId,
        string calldata reason
    ) external;
    
    function isValidDelegation(bytes32 delegationId) external view returns (bool);
    
    function verifyAuthorization(
        bytes32 delegationId,
        address declarant,
        bytes32 scopeHash
    ) external view returns (bool);
    
    function registerScope(
        bytes32 scopeId,
        string calldata name,
        string calldata description
    ) external;
    
    function getDelegation(bytes32 delegationId) external view returns (
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
    );
    
    function getProducerDelegations(address producer) external view returns (bytes32[] memory);
    
    function getDeclarantDelegations(address declarant) external view returns (bytes32[] memory);
    
    function getScope(bytes32 scopeId) external view returns (
        bytes32,
        string memory,
        string memory,
        bool
    );
    
    function setRegistrarAuthorization(address registrar, bool authorized) external;
    
    function getDelegationMessageHash(
        address signer,
        address counterparty,
        uint256 validUntil,
        bytes32 scopeHash
    ) external pure returns (bytes32);
}