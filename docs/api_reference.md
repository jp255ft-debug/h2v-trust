# H2V-Trust API Reference

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health

#### GET /health
Returns the service health status.

**Response:**
```json
{
  "status": "ok",
  "service": "h2v-trust"
}
```

### Batches

#### GET /api/v1/batches
List all batches with optional filtering.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum records to return
- `producer_id` (string, optional): Filter by producer
- `compliant_only` (bool, optional): Filter compliant batches only

**Response:**
```json
{
  "batches": [
    {
      "id": "string",
      "telemetry_id": 0,
      "producer_wallet": "string",
      "producer_id": "string",
      "facility_id": "string",
      "production_location": "string",
      "size_kg": 0.0,
      "is_compliant": true,
      "compliance_report": {},
      "batch_hash": "string",
      "telemetry": {},
      "created_at": "string"
    }
  ],
  "total": 0
}
```

#### GET /api/v1/batches/{batch_id}
Get a specific batch by ID.

#### GET /api/v1/batches/{batch_id}/compliance
Get compliance report for a specific batch.

### Certificates

#### GET /api/v1/certificates
List all certificates.

#### GET /api/v1/certificates/{certificate_id}
Get a specific certificate.

#### GET /api/v1/certificates/{certificate_id}/verify
Verify a certificate on-chain.

#### POST /api/v1/certificates/{certificate_id}/consume
Consume (surrender) a certificate for CBAM purposes.

**Request Body:**
```json
{
  "consumer_wallet": "string",
  "purpose": "cbam_surrender"
}
```

### Compliance

#### GET /api/v1/compliance/check/{batch_id}
Run a compliance check on a batch.

#### POST /api/v1/compliance/validate
Validate compliance with auditor wallet.

**Request Body:**
```json
{
  "batch_id": "string",
  "validator_wallet": "string"
}
```

### Delegation

#### GET /api/v1/delegation/status/{producer_id}
Get delegation status for a producer.

#### POST /api/v1/delegation/authorize
Authorize a declarant for CBAM delegation.

**Request Body:**
```json
{
  "producer_id": "string",
  "declarant_address": "string",
  "valid_until": "string (ISO datetime)"
}
```

#### POST /api/v1/delegation/revoke
Revoke an active delegation.

**Request Body:**
```json
{
  "producer_id": "string"
}
```

### Telemetry

#### POST /api/v1/telemetry
Send telemetry data from IoT sensors.

**Request Body:**
```json
{
  "sensor_id": "string",
  "timestamp": "string (ISO datetime)",
  "energy_source": "string",
  "power_generated_mwh": 0.0,
  "ghg_emissions": 0.0,
  "water_consumption_liters": 0.0,
  "water_source": "string"
}
```

### Reports

#### GET /api/v1/reports/cbam/{year}
Get CBAM report for a specific year.

#### GET /api/v1/reports/cbam/{year}/download
Download CBAM report as file.

## Error Responses

All endpoints return standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `422`: Validation Error
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message description"
}
```
