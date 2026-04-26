# CBAM Delegation Guide

## What is CBAM Delegation?

CBAM Delegation allows green hydrogen producers to authorize a third party (declarant) to submit CBAM declarations on their behalf. This is particularly useful for producers who may not have direct access to the EU CBAM reporting system.

## Delegation Flow

```
Producer                    Blockchain                   Declarant
   │                           │                           │
   ├── Authorize Delegation ──►│                           │
   │                           ├── Store Delegation ──────►│
   │                           │                           │
   │                           │◄── Verify Delegation ─────┤
   │                           │                           │
   │◄── Status Notification ──┤                           │
   │                           │                           │
   │                           │◄── Submit CBAM Report ────┤
   │                           │                           │
   ├── Revoke Delegation ────►│                           │
   │                           │                           │
```

## API Usage

### 1. Authorize Delegation

```bash
curl -X POST http://localhost:8000/api/v1/delegation/authorize \
  -H "Content-Type: application/json" \
  -d '{
    "producer_id": "prod_001",
    "declarant_address": "0xDeclarantWalletAddress",
    "valid_until": "2025-12-31T23:59:59Z"
  }'
```

### 2. Check Delegation Status

```bash
curl http://localhost:8000/api/v1/delegation/status/prod_001
```

### 3. Revoke Delegation

```bash
curl -X POST http://localhost:8000/api/v1/delegation/revoke \
  -H "Content-Type: application/json" \
  -d '{
    "producer_id": "prod_001"
  }'
```

## Smart Contract Integration

Delegations are recorded on-chain for transparency and immutability:

```solidity
// DelegationManager.sol
function authorizeDelegation(
    address declarant,
    uint256 validUntil
) external returns (uint256 delegationId);

function revokeDelegation(
    uint256 delegationId
) external;

function getDelegationStatus(
    address producer
) external view returns (
    address declarant,
    uint256 validUntil,
    bool isActive
);
```

## Security Considerations

1. **Wallet Security**: Use hardware wallets for delegation transactions
2. **Expiration**: Set reasonable expiration periods for delegations
3. **Revocation**: Revoke delegations immediately if compromised
4. **Audit Trail**: All delegation changes are recorded on-chain
5. **Multi-sig**: Consider multi-signature wallets for production environments

## Best Practices

1. **Regular Review**: Review active delegations monthly
2. **Short Durations**: Set delegation periods to 90 days or less
3. **Declarant Verification**: Verify declarant identity before authorization
4. **Backup Plans**: Have contingency plans for declarant unavailability
5. **Documentation**: Maintain records of all delegation changes
