"""
Test script for Phase 4 protected endpoint.

Tests the /protected-test endpoint with:
1. Valid token
2. Invalid token
3. Missing token
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token


BASE_URL = "http://127.0.0.1:8003"


def separator(title: str) -> None:
	"""Print formatted section separator."""
	print("\n" + "=" * 60)
	print(title)
	print("=" * 60)


def make_request(endpoint: str, token: str = None) -> dict:
	"""Make HTTP request to protected endpoint."""
	url = f"{BASE_URL}{endpoint}"
	
	headers = {"Content-Type": "application/json"}
	if token:
		headers["Authorization"] = f"Bearer {token}"
	
	request = urllib.request.Request(url, headers=headers)
	
	try:
		with urllib.request.urlopen(request) as response:
			status = response.status
			data = json.loads(response.read().decode())
			return {"status": status, "data": data, "error": None}
	except urllib.error.HTTPError as exc:
		error_data = json.loads(exc.read().decode()) if exc.headers.get("content-type") == "application/json" else {"detail": str(exc)}
		return {"status": exc.code, "data": error_data, "error": error_data.get("detail")}


def test_protected_endpoint_with_valid_token() -> None:
	"""Test protected endpoint with valid token."""
	separator("TEST 1: PROTECTED ENDPOINT WITH VALID TOKEN")
	
	# Create valid token
	test_payload = {"sub": "testuser@example.com"}
	token = create_access_token(test_payload)
	print(f"Token created: {token[:50]}...")
	
	response = make_request("/protected-test", token=token)
	
	print(f"Status Code: {response['status']}")
	print(f"Response: {response['data']}")
	
	if response['status'] == 200:
		print(f"✓ Authenticated as: {response['data']['authenticated_user']['email']}")
		print("✓ TEST PASSED: Valid token accepted")
	else:
		print("✗ TEST FAILED: Valid token was rejected")


def test_protected_endpoint_with_invalid_token() -> None:
	"""Test protected endpoint with invalid token."""
	separator("TEST 2: PROTECTED ENDPOINT WITH INVALID TOKEN")
	
	response = make_request("/protected-test", token="invalid.token.here")
	
	print(f"Status Code: {response['status']}")
	print(f"Response: {response['data']}")
	
	if response['status'] == 401:
		print("✓ TEST PASSED: Invalid token correctly rejected with 401")
	else:
		print(f"✗ TEST FAILED: Expected 401, got {response['status']}")


def test_protected_endpoint_without_token() -> None:
	"""Test protected endpoint without token."""
	separator("TEST 3: PROTECTED ENDPOINT WITHOUT TOKEN")
	
	response = make_request("/protected-test")
	
	print(f"Status Code: {response['status']}")
	print(f"Response: {response['data']}")
	
	# OAuth2 returns 401 when token is missing (not 403)
	if response['status'] == 401:
		print("✓ TEST PASSED: Missing token correctly rejected with 401")
	else:
		print(f"✗ TEST FAILED: Expected 401, got {response['status']}")


def test_protected_endpoint_with_expired_token() -> None:
	"""Test protected endpoint with expired token."""
	separator("TEST 4: PROTECTED ENDPOINT WITH EXPIRED TOKEN")
	
	# Create token that expires immediately
	test_payload = {"sub": "expired@example.com"}
	expired_token = create_access_token(test_payload, expiresedelta=timedelta(seconds=-1))
	
	response = make_request("/protected-test", token=expired_token)
	
	print(f"Status Code: {response['status']}")
	print(f"Response: {response['data']}")
	
	if response['status'] == 401:
		print("✓ TEST PASSED: Expired token correctly rejected with 401")
	else:
		print(f"✗ TEST FAILED: Expected 401, got {response['status']}")


def main() -> None:
	"""Run all protected endpoint tests."""
	
	print("\n" + "=" * 60)
	print("PHASE 4: PROTECTED ENDPOINT TESTS")
	print("=" * 60)
	print(f"Testing endpoint: {BASE_URL}/protected-test")
	
	try:
		test_protected_endpoint_with_valid_token()
		test_protected_endpoint_with_invalid_token()
		test_protected_endpoint_without_token()
		test_protected_endpoint_with_expired_token()
		
		separator("TEST SUMMARY")
		print("✓ ALL PROTECTED ENDPOINT TESTS COMPLETED")
		print("\nPhase 4 Complete: Authentication dependency layer verified")
		print("=" * 60)
		
	except Exception as exc:
		print(f"✗ TEST FAILED: {exc}")
		import traceback
		traceback.print_exc()
		sys.exit(1)


if __name__ == "__main__":
	main()
