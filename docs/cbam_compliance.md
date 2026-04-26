# CBAM Compliance Guide

## Overview

The Carbon Border Adjustment Mechanism (CBAM) is the EU's tool to put a fair price on the carbon emitted during the production of carbon-intensive goods entering the EU. H2V-Trust provides comprehensive support for CBAM compliance in green hydrogen production.

## CBAM Requirements for Green Hydrogen

### 1. GHG Emissions Threshold
- **Limit**: Maximum 3.4 kg CO₂e per kg H₂
- **Calculation**: Well-to-gate emissions including production and processing
- **Verification**: Via IoT telemetry and satellite monitoring

### 2. Water Consumption
- **Limit**: Maximum 20 liters per kg H₂
- **Sources**: Desalination, treated wastewater, surface water, groundwater, recycled
- **Monitoring**: Real-time flow meters and quality sensors

### 3. Energy Source
- **Requirement**: Must use renewable energy sources
- **Accepted**: Wind, solar, hydro, biomass
- **Verification**: Renewable Energy Certificates (RECs) and grid monitoring

### 4. Additionality
- **Requirement**: Hydrogen production must demonstrate environmental additionality
- **Verification**: Satellite monitoring of regional grid carbon intensity

## Compliance Flow

```
1. Telemetry Data Collection
   ↓
2. Batch Creation
   ↓
3. Automated Compliance Check
   ├── GHG Emissions ≤ 3.4 kgCO₂e/kgH₂
   ├── Water Consumption ≤ 20 L/kgH₂
   ├── Renewable Energy Source
   └── Additionality Verified
   ↓
4. Certificate Issuance (if compliant)
   ↓
5. Blockchain Registration
   ↓
6. CBAM Report Generation
```

## CBAM Report Components

- **Declared Emissions**: Total CO₂e emissions per batch
- **Saved Emissions**: Emissions avoided vs. grey hydrogen (9.3 kgCO₂e/kgH₂)
- **Certificate Eligibility**: Whether batch qualifies for CBAM certificate
- **Verification Status**: Blockchain verification confirmation

## Delegation Management

Producers can delegate CBAM declaration to authorized declarants:

1. **Authorize**: Producer creates delegation with declarant address
2. **Verify**: Declarant can verify delegation on-chain
3. **Report**: Declarant submits CBAM declaration on behalf of producer
4. **Revoke**: Producer can revoke delegation at any time

## Penalties

Non-compliant hydrogen faces:
- CBAM penalty of €50 per ton CO₂e
- Exclusion from green hydrogen certification
- Additional verification requirements

## Best Practices

1. **Real-time Monitoring**: Continuous telemetry data collection
2. **Regular Audits**: Periodic compliance verification
3. **Documentation**: Maintain complete production records
4. **Early Reporting**: Generate CBAM reports quarterly
5. **Blockchain Verification**: Use on-chain certificates for transparency
