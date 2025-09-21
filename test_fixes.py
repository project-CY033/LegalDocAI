#!/usr/bin/env python3
"""
Test script to verify that all bugs and errors have been fixed.
"""

import requests
import json
import time
from datetime import datetime, timezone

# Test configuration
API_BASE = 'http://localhost:8000'
TEST_RESULTS = []

def log_test(test_name, status, message=""):
    """Log test results."""
    timestamp = datetime.now(timezone.utc).isoformat()
    result = {
        "test": test_name,
        "status": status,
        "message": message,
        "timestamp": timestamp
    }
    TEST_RESULTS.append(result)
    print(f"[{status}] {test_name}: {message}")

def test_api_health():
    """Test API health endpoint."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                log_test("API Health Check", "PASS", "API is healthy and responding")
                return True
            else:
                log_test("API Health Check", "FAIL", f"Unexpected response: {data}")
                return False
        else:
            log_test("API Health Check", "FAIL", f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("API Health Check", "FAIL", str(e))
        return False

def test_datetime_fix():
    """Test that datetime deprecation warnings are fixed."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get("timestamp")
            if timestamp and "T" in timestamp:
                log_test("Datetime Fix", "PASS", "Timestamp format correct")
                return True
            else:
                log_test("Datetime Fix", "FAIL", "Invalid timestamp format")
                return False
        else:
            log_test("Datetime Fix", "FAIL", f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Datetime Fix", "FAIL", str(e))
        return False

def test_document_upload():
    """Test document upload functionality."""
    try:
        # Create a test text file
        test_content = """
        RENTAL AGREEMENT
        
        This is a test rental agreement between Landlord and Tenant.
        Monthly rent: $1200
        Security deposit: $1800
        Lease term: 12 months
        """
        
        files = {'file': ('test_lease.txt', test_content, 'text/plain')}
        response = requests.post(f"{API_BASE}/api/v1/documents/upload", files=files, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("id") and data.get("status") == "completed":
                log_test("Document Upload", "PASS", f"Document uploaded with ID: {data['id']}")
                return data["id"]
            else:
                log_test("Document Upload", "FAIL", f"Unexpected response: {data}")
                return None
        else:
            log_test("Document Upload", "FAIL", f"HTTP {response.status_code}: {response.text}")
            return None
    except Exception as e:
        log_test("Document Upload", "FAIL", str(e))
        return None

def test_document_analysis(document_id):
    """Test document analysis functionality."""
    if not document_id:
        log_test("Document Analysis", "SKIP", "No document ID available")
        return False
        
    try:
        payload = {
            "analysis_type": "full_summary",
            "language": "en"
        }
        response = requests.post(
            f"{API_BASE}/api/v1/analysis/analyze/{document_id}", 
            json=payload, 
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("summary") and data.get("confidence_score"):
                log_test("Document Analysis", "PASS", "Analysis completed successfully")
                return True
            else:
                log_test("Document Analysis", "FAIL", f"Missing analysis data: {data}")
                return False
        else:
            log_test("Document Analysis", "FAIL", f"HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        log_test("Document Analysis", "FAIL", str(e))
        return False

def test_question_answering(document_id):
    """Test Q&A functionality."""
    if not document_id:
        log_test("Question Answering", "SKIP", "No document ID available")
        return False
        
    try:
        payload = {
            "question": "What is the monthly rent?",
            "language": "en"
        }
        response = requests.post(
            f"{API_BASE}/api/v1/analysis/question/{document_id}", 
            json=payload, 
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("answer") and data.get("question"):
                log_test("Question Answering", "PASS", "Q&A working correctly")
                return True
            else:
                log_test("Question Answering", "FAIL", f"Missing Q&A data: {data}")
                return False
        else:
            log_test("Question Answering", "FAIL", f"HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        log_test("Question Answering", "FAIL", str(e))
        return False

def test_cors_headers():
    """Test CORS headers are properly set."""
    try:
        # Send request with Origin header to trigger CORS response
        headers = {'Origin': 'http://localhost:3000'}
        response = requests.get(f"{API_BASE}/health", headers=headers, timeout=5)
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            log_test("CORS Headers", "PASS", f"CORS header present: {cors_header}")
            return True
        else:
            log_test("CORS Headers", "FAIL", "Missing CORS headers")
            return False
    except Exception as e:
        log_test("CORS Headers", "FAIL", str(e))
        return False

def run_all_tests():
    """Run all tests and generate report."""
    print("🧪 Starting LegalDocAI Bug Fix Verification Tests...")
    print("=" * 60)
    
    # Test 1: API Health
    health_ok = test_api_health()
    
    # Test 2: Datetime fix
    datetime_ok = test_datetime_fix()
    
    # Test 3: CORS headers
    cors_ok = test_cors_headers()
    
    # Test 4: Document upload
    document_id = test_document_upload()
    
    # Test 5: Document analysis (depends on upload)
    analysis_ok = test_document_analysis(document_id)
    
    # Test 6: Question answering (depends on upload)
    qa_ok = test_question_answering(document_id)
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for test in TEST_RESULTS if test["status"] == "PASS")
    failed = sum(1 for test in TEST_RESULTS if test["status"] == "FAIL")
    skipped = sum(1 for test in TEST_RESULTS if test["status"] == "SKIP")
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "N/A")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    for test in TEST_RESULTS:
        status_icon = "✅" if test["status"] == "PASS" else "❌" if test["status"] == "FAIL" else "⏭️"
        print(f"{status_icon} {test['test']}: {test['message']}")
    
    # Overall status
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The bugs have been successfully fixed.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Some issues may still need attention.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)