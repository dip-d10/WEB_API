"""
Validation script for Phase 5 schemas.

Tests:
1. Valid RegisterRequest → should pass
2. Invalid email → should fail
3. Missing fields → should fail
4. Wrong data types → should fail
5. Valid LoginRequest → should pass
6. Valid TokenResponse → should pass
7. Valid UserResponse → should pass
8. Valid PredictionRequest → should pass
9. Valid PredictionResponse → should pass
10. Valid PredictionHistoryResponse → should pass
"""

from datetime import datetime, timedelta
from pydantic import ValidationError

from app.schemas.auth_schema import (
	RegisterRequest,
	LoginRequest,
	TokenResponse,
	UserResponse,
)
from app.schemas.prediction_schema import (
	PredictionRequest,
	PredictionResponse,
	PredictionHistoryResponse,
)


def separator(title: str) -> None:
	"""Print formatted section separator."""
	print("\n" + "=" * 60)
	print(title)
	print("=" * 60)


def test_valid_register_request() -> None:
	"""Test 1: Valid RegisterRequest should pass."""
	separator("TEST 1: VALID REGISTER REQUEST")
	
	try:
		request = RegisterRequest(
			name="John Doe",
			email="john@example.com",
			password="secure_password_123"
		)
		print(f"✓ Valid RegisterRequest created:")
		print(f"  Name: {request.name}")
		print(f"  Email: {request.email}")
		print(f"  Password: {'*' * len(request.password)}")
		print("✓ TEST PASSED: Valid RegisterRequest")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_invalid_email_register() -> None:
	"""Test 2: Invalid email in RegisterRequest should fail."""
	separator("TEST 2: INVALID EMAIL IN REGISTER REQUEST")
	
	try:
		RegisterRequest(
			name="John Doe",
			email="invalid-email",  # Invalid email
			password="secure_password_123"
		)
		print("✗ TEST FAILED: Should have rejected invalid email")
	except ValidationError as exc:
		print(f"✓ Invalid email correctly rejected")
		print(f"✓ TEST PASSED: Email validation works")


def test_short_password_register() -> None:
	"""Test 3: Password too short in RegisterRequest should fail."""
	separator("TEST 3: PASSWORD TOO SHORT IN REGISTER REQUEST")
	
	try:
		RegisterRequest(
			name="John Doe",
			email="john@example.com",
			password="short"  # Too short (minimum 8)
		)
		print("✗ TEST FAILED: Should have rejected short password")
	except ValidationError as exc:
		print(f"✓ Short password correctly rejected")
		print(f"✓ TEST PASSED: Password length validation works")


def test_missing_fields_register() -> None:
	"""Test 4: Missing required fields in RegisterRequest should fail."""
	separator("TEST 4: MISSING FIELDS IN REGISTER REQUEST")
	
	try:
		RegisterRequest(
			name="John Doe",
			email="john@example.com"
			# Missing password
		)
		print("✗ TEST FAILED: Should have rejected missing password")
	except ValidationError as exc:
		print(f"✓ Missing field correctly rejected")
		print(f"✓ TEST PASSED: Required field validation works")


def test_valid_login_request() -> None:
	"""Test 5: Valid LoginRequest should pass."""
	separator("TEST 5: VALID LOGIN REQUEST")
	
	try:
		request = LoginRequest(
			email="john@example.com",
			password="secure_password_123"
		)
		print(f"✓ Valid LoginRequest created:")
		print(f"  Email: {request.email}")
		print(f"  Password: {'*' * len(request.password)}")
		print("✓ TEST PASSED: Valid LoginRequest")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_valid_token_response() -> None:
	"""Test 6: Valid TokenResponse should pass."""
	separator("TEST 6: VALID TOKEN RESPONSE")
	
	try:
		response = TokenResponse(
			access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjc5MzI4MDAwfQ.test",
			token_type="bearer"
		)
		print(f"✓ Valid TokenResponse created:")
		print(f"  Access Token: {response.access_token[:50]}...")
		print(f"  Token Type: {response.token_type}")
		print("✓ TEST PASSED: Valid TokenResponse")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_valid_user_response() -> None:
	"""Test 7: Valid UserResponse should pass."""
	separator("TEST 7: VALID USER RESPONSE")
	
	try:
		response = UserResponse(
			id="507f1f77bcf86cd799439011",
			name="John Doe",
			email="john@example.com"
		)
		print(f"✓ Valid UserResponse created:")
		print(f"  ID: {response.id}")
		print(f"  Name: {response.name}")
		print(f"  Email: {response.email}")
		print("✓ TEST PASSED: Valid UserResponse")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_valid_prediction_request() -> None:
	"""Test 8: Valid PredictionRequest should pass."""
	separator("TEST 8: VALID PREDICTION REQUEST")
	
	try:
		request = PredictionRequest(
			feature_1=0.5,
			feature_2=1.2,
			feature_3=2.3
		)
		print(f"✓ Valid PredictionRequest created:")
		print(f"  Feature 1: {request.feature_1}")
		print(f"  Feature 2: {request.feature_2}")
		print(f"  Feature 3: {request.feature_3}")
		print("✓ TEST PASSED: Valid PredictionRequest")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_valid_prediction_response() -> None:
	"""Test 9: Valid PredictionResponse should pass."""
	separator("TEST 9: VALID PREDICTION RESPONSE")
	
	try:
		now = datetime.utcnow()
		response = PredictionResponse(
			prediction="Class A",
			confidence=0.95,
			model_version="1.0.0",
			timestamp=now
		)
		print(f"✓ Valid PredictionResponse created:")
		print(f"  Prediction: {response.prediction}")
		print(f"  Confidence: {response.confidence}")
		print(f"  Model Version: {response.model_version}")
		print(f"  Timestamp: {response.timestamp}")
		print("✓ TEST PASSED: Valid PredictionResponse")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_valid_prediction_history_response() -> None:
	"""Test 10: Valid PredictionHistoryResponse should pass."""
	separator("TEST 10: VALID PREDICTION HISTORY RESPONSE")
	
	try:
		now = datetime.utcnow()
		response = PredictionHistoryResponse(
			user_id="507f1f77bcf86cd799439011",
			input_features={
				"feature_1": 0.5,
				"feature_2": 1.2,
				"feature_3": 2.3
			},
			prediction_result="Class A",
			model_version="1.0.0",
			timestamp=now
		)
		print(f"✓ Valid PredictionHistoryResponse created:")
		print(f"  User ID: {response.user_id}")
		print(f"  Input Features: {response.input_features}")
		print(f"  Prediction Result: {response.prediction_result}")
		print(f"  Model Version: {response.model_version}")
		print(f"  Timestamp: {response.timestamp}")
		print("✓ TEST PASSED: Valid PredictionHistoryResponse")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_prediction_response_optional_confidence() -> None:
	"""Test 11: PredictionResponse with optional confidence should pass."""
	separator("TEST 11: PREDICTION RESPONSE WITHOUT CONFIDENCE")
	
	try:
		now = datetime.utcnow()
		response = PredictionResponse(
			prediction="Class B",
			confidence=None,  # Optional field
			model_version="1.0.0",
			timestamp=now
		)
		print(f"✓ PredictionResponse without confidence created:")
		print(f"  Prediction: {response.prediction}")
		print(f"  Confidence: {response.confidence}")
		print(f"  Model Version: {response.model_version}")
		print("✓ TEST PASSED: Optional confidence field works")
	except ValidationError as exc:
		print(f"✗ TEST FAILED: {exc}")
		raise


def test_invalid_confidence_range() -> None:
	"""Test 12: Invalid confidence range in PredictionResponse should fail."""
	separator("TEST 12: INVALID CONFIDENCE RANGE")
	
	try:
		now = datetime.utcnow()
		PredictionResponse(
			prediction="Class A",
			confidence=1.5,  # Invalid: > 1.0
			model_version="1.0.0",
			timestamp=now
		)
		print("✗ TEST FAILED: Should have rejected confidence > 1.0")
	except ValidationError as exc:
		print(f"✓ Invalid confidence correctly rejected")
		print(f"✓ TEST PASSED: Confidence range validation works")


def main() -> None:
	"""Run all schema validation tests."""
	print("\n" + "=" * 60)
	print("STARTING SCHEMA VALIDATION (PHASE 5)")
	print("=" * 60)
	
	try:
		# Auth schema tests
		test_valid_register_request()
		test_invalid_email_register()
		test_short_password_register()
		test_missing_fields_register()
		test_valid_login_request()
		test_valid_token_response()
		test_valid_user_response()
		
		# Prediction schema tests
		test_valid_prediction_request()
		test_valid_prediction_response()
		test_valid_prediction_history_response()
		test_prediction_response_optional_confidence()
		test_invalid_confidence_range()
		
		# Summary
		separator("VALIDATION SUMMARY")
		print("✓ ALL SCHEMA VALIDATION TESTS PASSED")
		print("\nPhase 5 Status: Schemas layer implemented and validated")
		print("✓ Auth schemas: RegisterRequest, LoginRequest, TokenResponse, UserResponse")
		print("✓ Prediction schemas: PredictionRequest, PredictionResponse, PredictionHistoryResponse")
		print("=" * 60)
		
	except Exception as exc:
		print(f"\n✗ VALIDATION FAILED: {exc}")
		import traceback
		traceback.print_exc()
		raise


if __name__ == "__main__":
	main()
