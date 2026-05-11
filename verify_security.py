import asyncio
from datetime import timedelta

from app.core.security import (
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from app.logger import get_logger


logger = get_logger(__name__)


def test_password_flow() -> None:
    """Test password hashing and verification."""
    logger.info("=" * 60)
    logger.info("TESTING PASSWORD FLOW")
    logger.info("=" * 60)
    
    plain_password = "secure_password_123"
    logger.info("Plain password: %s", plain_password)
    
    # Test hashing
    hashed = hash_password(plain_password)
    logger.info("Hashed password: %s...", hashed[:30])
    
    # Test verification - correct password
    is_correct = verify_password(plain_password, hashed)
    logger.info("Verify correct password: %s", is_correct)
    assert is_correct is True, "Password verification failed for correct password"
    
    # Test verification - incorrect password
    is_incorrect = verify_password("wrong_password", hashed)
    logger.info("Verify incorrect password: %s", is_incorrect)
    assert is_incorrect is False, "Password verification should fail for incorrect password"
    
    logger.info("✓ Password flow test PASSED\n")


def test_jwt_flow() -> None:
    """Test JWT token creation and verification."""
    logger.info("=" * 60)
    logger.info("TESTING JWT TOKEN FLOW")
    logger.info("=" * 60)
    
    # Create token
    payload = {"sub": "user@example.com", "user_id": "12345"}
    logger.info("Payload: %s", payload)
    
    token = create_access_token(data=payload)
    logger.info("Created token: %s...", token[:50])
    
    # Verify token
    decoded = verify_access_token(token)
    logger.info("Decoded payload: %s", decoded)
    assert decoded.get("sub") == payload["sub"], "Subject mismatch in decoded token"
    assert decoded.get("user_id") == payload["user_id"], "User ID mismatch in decoded token"
    logger.info("✓ Token payload verified correctly")
    
    # Test expired token
    logger.info("\nTesting token expiration...")
    expired_payload = {"sub": "test@example.com"}
    expired_token = create_access_token(
        data=expired_payload,
        expiresedelta=timedelta(seconds=-1)  # Already expired
    )
    logger.info("Created expired token: %s...", expired_token[:50])
    
    try:
        verify_access_token(expired_token)
        logger.error("✗ Should have raised exception for expired token")
        assert False, "Expired token should raise exception"
    except ValueError as e:
        logger.info("✓ Expired token correctly rejected: %s", str(e))
    
    # Test invalid token
    logger.info("\nTesting invalid token...")
    try:
        verify_access_token("invalid.token.here")
        logger.error("✗ Should have raised exception for invalid token")
        assert False, "Invalid token should raise exception"
    except ValueError as e:
        logger.info("✓ Invalid token correctly rejected: %s", str(e))
    
    logger.info("✓ JWT flow test PASSED\n")


def main() -> None:
    """Run all security tests."""
    logger.info("\n" + "=" * 60)
    logger.info("STARTING SECURITY UTILITIES VALIDATION")
    logger.info("=" * 60 + "\n")
    
    try:
        test_password_flow()
        test_jwt_flow()
        
        logger.info("=" * 60)
        logger.info("✓ ALL SECURITY TESTS PASSED")
        logger.info("=" * 60)
    except Exception as exc:
        logger.exception("✗ SECURITY TEST FAILED: %s", exc)
        raise


if __name__ == "__main__":
    main()
