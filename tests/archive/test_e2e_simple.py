#!/usr/bin/env python3
"""End-to-end test for H2V-Trust flow (Windows compatible)."""

import requests
import json
import sys
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
API_KEY = "test-secret-key-for-local-development-12345"  # From backend/config.py

def make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make HTTP request to backend."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return {"error": str(e)}

def test_scenario_1_compliant_telemetry() -> Dict:
    """Scenario 1: Send compliant telemetry (2.8 kgCO2/kgH2)."""
    print("\n=== Scenario 1: Compliant Telemetry ===")
    
    telemetry_data = {
        "sensor_id": "sensor_test_001",
        "timestamp": "2026-04-18T10:00:00Z",
        "energy_source": "solar",
        "power_generated_mwh": 10.5,
        "ghg_emissions_kgCO2_per_kgH2": 2.8,
        "water_consumption_liters": 150.0,
        "water_source": "desalination"
    }
    
    print(f"Sending telemetry: {json.dumps(telemetry_data, indent=2)}")
    result = make_request("POST", "/api/v1/telemetry", telemetry_data)
    
    if "error" in result:
        print(f"FAILED: {result['error']}")
        return {"success": False, "result": result}
    
    print(f"SUCCESS! Response: {json.dumps(result, indent=2)}")
    
    # Extract IDs for later tests
    batch_id = result.get("batch_id")
    certificate_id = result.get("certificate_id")
    
    if batch_id and certificate_id:
        print(f"Batch ID: {batch_id}")
        print(f"Certificate ID: {certificate_id}")
        return {
            "success": True, 
            "batch_id": batch_id,
            "certificate_id": certificate_id,
            "result": result
        }
    else:
        print("FAIL: Missing batch_id or certificate_id in response")
        return {"success": False, "result": result}

def test_scenario_2_non_compliant_telemetry() -> Dict:
    """Scenario 2: Send non-compliant telemetry (5.0 kgCO2/kgH2)."""
    print("\n=== Scenario 2: Non-Compliant Telemetry ===")
    
    telemetry_data = {
        "sensor_id": "sensor_test_002",
        "timestamp": "2026-04-18T10:05:00Z",
        "energy_source": "solar",
        "power_generated_mwh": 10.5,
        "ghg_emissions_kgCO2_per_kgH2": 5.0,  # Above 3.4 limit
        "water_consumption_liters": 150.0,
        "water_source": "desalination"
    }
    
    print(f"Sending non-compliant telemetry (5.0 kgCO2/kgH2)...")
    result = make_request("POST", "/api/v1/telemetry", telemetry_data)
    
    # Expecting error for non-compliant data
    if "error" in result:
        print(f"EXPECTED FAILURE: {result.get('error', 'No error details')}")
        return {"success": True, "expected_failure": True, "result": result}
    else:
        print(f"UNEXPECTED SUCCESS for non-compliant data")
        print(f"Response: {json.dumps(result, indent=2)}")
        return {"success": False, "result": result}

def test_scenario_3_certificate_verification(batch_id: str, certificate_id: str) -> Dict:
    """Scenario 3: Verify certificate and batch compliance."""
    print("\n=== Scenario 3: Certificate Verification ===")
    
    # Get certificate
    print(f"Getting certificate {certificate_id}...")
    cert_result = make_request("GET", f"/api/v1/certificates/{certificate_id}")
    
    if "error" in cert_result:
        print(f"FAILED to get certificate: {cert_result['error']}")
        return {"success": False, "result": cert_result}
    
    print(f"CERTIFICATE RETRIEVED: {json.dumps(cert_result, indent=2)}")
    
    # Get batch compliance
    print(f"Getting batch compliance for {batch_id}...")
    compliance_result = make_request("GET", f"/api/v1/batches/{batch_id}/compliance")
    
    if "error" in compliance_result:
        print(f"FAILED to get compliance: {compliance_result['error']}")
        return {"success": False, "result": compliance_result}
    
    print(f"COMPLIANCE REPORT: {json.dumps(compliance_result, indent=2)}")
    
    return {
        "success": True,
        "certificate": cert_result,
        "compliance": compliance_result
    }

def test_scenario_4_certificate_consumption(certificate_id: str) -> Dict:
    """Scenario 4: Consume certificate to prevent double counting."""
    print("\n=== Scenario 4: Certificate Consumption ===")
    
    # Consume certificate
    print(f"Consuming certificate {certificate_id}...")
    consume_result = make_request("POST", f"/api/v1/certificates/{certificate_id}/consume")
    
    if "error" in consume_result:
        print(f"FAILED to consume: {consume_result['error']}")
        return {"success": False, "result": consume_result}
    
    print(f"CONSUMPTION RESULT: {json.dumps(consume_result, indent=2)}")
    
    # Verify consumption status
    print(f"Verifying consumption status...")
    cert_result = make_request("GET", f"/api/v1/certificates/{certificate_id}")
    
    if "error" in cert_result:
        print(f"FAILED to verify: {cert_result['error']}")
        return {"success": False, "result": cert_result}
    
    is_consumed = cert_result.get("certificate", {}).get("is_consumed", False)
    if is_consumed:
        print(f"CERTIFICATE successfully marked as consumed")
    else:
        print(f"CERTIFICATE not marked as consumed")
        
    # Try to consume again (should fail)
    print(f"Attempting to consume again (should fail)...")
    second_consume = make_request("POST", f"/api/v1/certificates/{certificate_id}/consume")
    
    if "error" in second_consume:
        print(f"CORRECTLY rejected double consumption")
    else:
        print(f"SHOULD HAVE rejected double consumption")
        
    return {
        "success": is_consumed,
        "consume_result": consume_result,
        "verification": cert_result,
        "double_consume_blocked": "error" in second_consume
    }

def main():
    """Run all test scenarios."""
    print("=" * 60)
    print("H2V-Trust End-to-End Test")
    print("=" * 60)
    
    # Check backend health
    print("Checking backend health...")
    health = make_request("GET", "/health")
    if "error" in health:
        print(f"BACKEND NOT HEALTHY: {health['error']}")
        print("Make sure backend is running: venv\\Scripts\\python -m uvicorn backend.main:app --reload")
        return 1
    
    print(f"Backend healthy: {health}")
    
    # Run scenarios
    results = {}
    
    # Scenario 1: Compliant telemetry
    scenario1 = test_scenario_1_compliant_telemetry()
    results["scenario1"] = scenario1
    
    if not scenario1.get("success"):
        print("Scenario 1 failed, skipping remaining tests")
        return 1
    
    batch_id = scenario1.get("batch_id")
    certificate_id = scenario1.get("certificate_id")
    
    # Scenario 2: Non-compliant telemetry
    scenario2 = test_scenario_2_non_compliant_telemetry()
    results["scenario2"] = scenario2
    
    # Scenario 3: Certificate verification
    scenario3 = test_scenario_3_certificate_verification(batch_id, certificate_id)
    results["scenario3"] = scenario3
    
    # Scenario 4: Certificate consumption
    scenario4 = test_scenario_4_certificate_consumption(certificate_id)
    results["scenario4"] = scenario4
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    successes = sum(1 for k, v in results.items() if v.get("success"))
    total = len(results)
    
    print(f"Scenarios passed: {successes}/{total}")
    
    for name, result in results.items():
        status = "PASS" if result.get("success") else "FAIL"
        print(f"{name}: {status}")
    
    if successes == total:
        print("\nALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Start frontend: cd frontend && npm run dev")
        print("2. Open http://localhost:3000/auditor")
        print("3. Enter batch_id to verify certificate")
        return 0
    else:
        print(f"\n{total - successes} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())