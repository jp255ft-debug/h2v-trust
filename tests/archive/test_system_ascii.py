#!/usr/bin/env python3
"""Test to verify H2V-Trust system is working correctly."""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_KEY = "test-secret-key-for-local-development-12345"  # From simulator.py

def test_health():
    """Test health endpoint."""
    print("1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print(f"   [OK] Health OK: {response.json()}")
        return True
    else:
        print(f"   [ERROR] Health failed: {response.status_code}")
        return False

def test_telemetry_endpoint():
    """Test telemetry endpoint with compliant data."""
    print("\n2. Testing telemetry endpoint...")
    
    payload = {
        "sensor_id": "electrolyzer_01",
        "timestamp": datetime.now().isoformat() + "Z",
        "energy_source": "wind",
        "power_generated_mwh": 12.5,
        "ghg_emissions_kgCO2_per_kgH2": 2.8,
        "water_consumption_liters": 150,
        "water_source": "desalination"
    }
    
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    
    print(f"   Sending payload: {json.dumps(payload, indent=4)}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/telemetry", json=payload, headers=headers)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   [OK] Telemetry accepted!")
            print(f"   Batch ID: {result.get('batch_id')}")
            print(f"   Compliant: {result.get('is_compliant')}")
            print(f"   Certificate ID: {result.get('certificate_id')}")
            return True, result.get('batch_id')
        else:
            print(f"   [ERROR] Telemetry failed: {response.text}")
            return False, None
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False, None

def test_batches_endpoint():
    """Test batches endpoint."""
    print("\n3. Testing batches endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/batches")
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   [OK] Batches retrieved: {len(result.get('batches', []))} batches")
            return True
        else:
            print(f"   [ERROR] Batches failed: {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False

def test_compliance_endpoint():
    """Test compliance check endpoint."""
    print("\n4. Testing compliance endpoint...")
    
    payload = {
        "emissions_kgco2_per_kgh2": 2.5,
        "energy_source": "solar",
        "water_source": "desalination",
        "water_liters_per_kg": 12.0,
        "batch_size_kg": 1500.0,
        "producer_id": "prod_test_001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/compliance/check", json=payload)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   [OK] Compliance check successful")
            print(f"   Is compliant: {result.get('is_compliant')}")
            print(f"   CBAM compliant: {result.get('cbam_compliant')}")
            return True
        else:
            print(f"   [ERROR] Compliance check failed: {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("H2V-TRUST SYSTEM VERIFICATION TEST")
    print("=" * 60)
    
    # Check if backend is running
    if not test_health():
        print("\n[ERROR] Backend not running. Please start it with:")
        print("   uvicorn backend.main:app --reload --port 8000")
        return 1
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Health (already done)
    tests_passed += 1
    
    # Test 2: Telemetry
    telemetry_ok, batch_id = test_telemetry_endpoint()
    if telemetry_ok:
        tests_passed += 1
    
    # Test 3: Batches
    if test_batches_endpoint():
        tests_passed += 1
    
    # Test 4: Compliance
    if test_compliance_endpoint():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("\n[SUCCESS] ALL TESTS PASSED! System is fully functional.")
        print("\nNext steps:")
        print("1. Start frontend: cd frontend && npm run dev")
        print("2. Open browser: http://localhost:3000")
        print("3. Run IoT simulator: python iot/simulator.py")
        return 0
    elif tests_passed >= 2:
        print(f"\n[WARNING] {total_tests - tests_passed} test(s) failed but core system is working.")
        print("Check API endpoints and database connection.")
        return 1
    else:
        print("\n[ERROR] System has major issues. Check backend logs.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())