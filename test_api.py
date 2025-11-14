#!/usr/bin/env python3
"""
Test script for PDF Filler API
"""

import requests
import sys
import os
from pathlib import Path

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:8000')
EXCEL_FILE = 'Letter_of_Representation_Sample_Data.xlsx'

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print(f"✓ Health check passed: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        response.raise_for_status()
        print(f"✓ Root endpoint passed: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def test_fill_pdf():
    """Test PDF filling endpoint"""
    print("\nTesting PDF filling...")

    if not Path(EXCEL_FILE).exists():
        print(f"✗ Excel file not found: {EXCEL_FILE}")
        return False

    try:
        with open(EXCEL_FILE, 'rb') as f:
            files = {'file': (EXCEL_FILE, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(f"{API_URL}/fill-pdf", files=files)
            response.raise_for_status()

        # Save output
        output_file = 'test_filled_output.pdf'
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"✓ PDF filling passed: {output_file} created")
        print(f"  File size: {len(response.content)} bytes")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"✗ PDF filling failed: HTTP {e.response.status_code}")
        print(f"  Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"✗ PDF filling failed: {e}")
        return False

def test_invalid_file():
    """Test with invalid file type"""
    print("\nTesting invalid file type...")

    # Create a dummy text file
    dummy_file = 'test_dummy.txt'
    with open(dummy_file, 'w') as f:
        f.write('This is not an Excel file')

    try:
        with open(dummy_file, 'rb') as f:
            files = {'file': (dummy_file, f, 'text/plain')}
            response = requests.post(f"{API_URL}/fill-pdf", files=files)

        if response.status_code == 400:
            print(f"✓ Invalid file correctly rejected: {response.status_code}")
            return True
        else:
            print(f"✗ Expected 400, got {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    finally:
        # Clean up
        if Path(dummy_file).exists():
            os.remove(dummy_file)

def test_cleanup():
    """Test cleanup endpoint"""
    print("\nTesting cleanup endpoint...")
    try:
        response = requests.delete(f"{API_URL}/cleanup")
        response.raise_for_status()
        print(f"✓ Cleanup passed: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PDF Filler API Test Suite")
    print("=" * 60)
    print(f"Testing API at: {API_URL}")
    print("=" * 60)

    tests = [
        ('Health Check', test_health),
        ('Root Endpoint', test_root),
        ('Fill PDF', test_fill_pdf),
        ('Invalid File Type', test_invalid_file),
        ('Cleanup', test_cleanup),
    ]

    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
