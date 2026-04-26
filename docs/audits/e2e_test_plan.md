# H2V-Trust End-to-End Test Plan

## Overview
Validate the complete flow: Producer → IoT Telemetry → CBAM Compliance → Blockchain Minting → Consumer Verification

## Current Environment Status
- ✅ Backend: Running at `http://localhost:8000` (health check OK)
- ❌ Hardhat Node: Not running (needs to be started)
- ❌ Frontend: Not running (needs to be started)
- ✅ Database: SQLite initialized

## Test Scenarios

### Scenario 1: Successful Compliance & Certificate Minting
**Objective:** Send telemetry with emissions 2.8 kgCO₂/kgH₂ (below CBAM limit of 3.4) → should create batch and mint certificate

**Steps:**
1. POST `/telemetry` with valid data:
   - `ghg_kgco2_per_kgh2`: 2.8
   - `water_source`: "desalination"
   - `water_liters_per_kgh2`: 15
   - `energy_source`: "solar"
   - `energy_kwh_per_kgh2`: 50
2. Verify response: `201 Created` with `batch_id` and `certificate_id`
3. Check database: Batch and Certificate records created
4. Verify blockchain: Certificate minted on-chain (if Hardhat running)

### Scenario 2: Compliance Failure
**Objective:** Send telemetry with emissions 5.0 kgCO₂/kgH₂ (above limit) → should reject

**Steps:**
1. POST `/telemetry` with non-compliant data:
   - `ghg_kgco2_per_kgh2`: 5.0
   - Other fields same as Scenario 1
2. Verify response: `400 Bad Request` or similar error
3. Check database: No batch/certificate created

### Scenario 3: Certificate Verification by Consumer
**Objective:** Consumer verifies certificate authenticity

**Steps:**
1. GET `/certificates/{certificate_id}` from Scenario 1
2. Verify response includes certificate details and on-chain proof
3. GET `/batches/{batch_id}/compliance` to see compliance report
4. Verify all data matches original telemetry

### Scenario 4: Certificate Consumption (Prevent Double Counting)
**Objective:** Mark certificate as consumed when H2 is used

**Steps:**
1. POST `/certificates/{certificate_id}/consume`
2. Verify response: `200 OK` with `is_consumed: true`
3. GET `/certificates/{certificate_id}` to confirm consumption status
4. Attempt to consume again → should fail (already consumed)

### Scenario 5: Frontend Verification
**Objective:** Use web interface to verify certificate

**Steps:**
1. Start frontend: `cd frontend && npm run dev`
2. Access `http://localhost:3000/auditor`
3. Enter `batch_id` from Scenario 1
4. Verify: QR code displayed, certificate details shown, compliance status visible

## Implementation Plan

### 1. Start Missing Services
- Start Hardhat node: `cd contracts && npx hardhat node`
- Start frontend: `cd frontend && npm run dev`

### 2. Create Test Script (`test_e2e.py`)
- Use `requests` library for API calls
- Use `web3.py` for blockchain verification (if Hardhat running)
- Implement all 5 scenarios
- Generate detailed report with success/failure status

### 3. Manual Frontend Test
- Open browser to `http://localhost:3000/auditor`
- Test with valid and invalid batch IDs
- Take screenshots for documentation

### 4. Generate Test Report
- Document results in `e2e_test_report.md`
- Include screenshots, API responses, error logs
- Suggest improvements for next iteration

## Success Criteria
- All 5 scenarios execute without critical errors
- Blockchain integration works (certificates minted and verified)
- Frontend displays certificate data correctly
- Database persists all transactions
- API responses follow expected formats

## Risks & Mitigations
- **Hardhat not running**: Use mock blockchain responses for testing
- **Frontend issues**: Test API independently first
- **Database errors**: Ensure SQLite file is writable
- **API authentication**: Use test API key or disable auth for testing