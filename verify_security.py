import asyncio
from datetime import timedelta

from app.core.security import (
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)


def test_password_flow() -> None:
    """Test password hashing and verification."""
    print("=" * 60)
    print("TESTING PASSWORD FLOW")
    print("=" * 60)
    
    plain_password = "secure_password_123"
    print(f"Plain password: {plain_password}")
    
    # Test hashing
    hashed = hash_password(plain_password)
    print(f"Hashed password: {hashed[:30]}...")
    
    # Test verification - correct password
    is_correct = verify_password(plain_password, hashed)
    print(f"Verify correct password: {is_correct}")
    assert is_correct is True, "Password verification failed for correct password"
    
    # Test verification - incorrect password
    is_incorrect = verify_password("wrong_password", hashed)
    print(f"Verify incorrect password: {is_incorrect}")
    assert is_incorrect is False, "Password verification should fail for incorrect password"
    
    print("✓ Password flow test PASSED\n")


def test_jwt_flow() -> None:
    """Test JWT token creation and verification."""
    print("=" * 60)
    print("TESTING JWT TOKEN FLOW")
    print("=" * 60)
    
    # Create token
    payload = {"sub": "user@example.com", "user_id": "12345"}
    print(f"Payload: {payload}")
    
    token = create_access_token(data=payload)
    print(f"Created token: {token[:50]}...")
    
    # Verify token
    decoded = verify_access_token(token)
    print(f"Decoded payload: {decoded}")
    assert decoded.get("sub") == payload["sub"], "Subject mismatch in decoded token"
    assert decoded.get("user_id") == payload["user_id"], "User ID mismatch in decoded token"
    print("✓ Token payload verified correctly")
    
    # Test expired token
    print("\nTesting token expiration...")
    expired_payload = {"sub": "test@example.com"}
    expired_token = create_access_token(
        data=expired_payload,
        expiresedelta=timedelta(seconds=-1)  # Already expired
    )
    print(f"Created expired token: {expired_token[:50]}...")
    
    try:
        verify_access_token(expired_token)
        print("✗ Should have raised exception for expired token")
        assert False, "Expired token should raise exception"
    except ValueError as e:
        print(f"✓ Expired token correctly rejected: {str(e)}")
    
    # Test invalid token
    print("\nTesting invalid token...")
    try:
        verify_access_token("invalid.token.here")
        print("✗ Should have raised exception for invalid token")
        assert False, "Invalid token should raise exception"
    except ValueError as e:
        print(f"✓ Invalid token correctly rejected: {str(e)}")
    
    print("✓ JWT flow test PASSED\n")


def main() -> None:
    """Run all security tests."""
    print("\n" + "=" * 60)
    print("STARTING SECURITY UTILITIES VALIDATION")
    print("=" * 60 + "\n")
    
    try:
        test_password_flow()
        test_jwt_flow()
        
        print("=" * 60)
        print("✓ ALL SECURITY TESTS PASSED")
        print("=" * 60)
    except Exception as exc:
        print(f"✗ SECURITY TEST FAILED: {exc}")
        raise


if __name__ == "__main__":
    main()
