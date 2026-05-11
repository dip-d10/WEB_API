from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.logger import get_logger


logger = get_logger(__name__)

# Password hashing configuration
PASSWORD_HASH_ROUNDS = 12


def hash_password(password: str) -> str:
	"""
	Hash a plain password using bcrypt.
	
	Args:
		password: Plain text password (max 72 bytes enforced by bcrypt)
		
	Returns:
		Hashed password string
	"""
	if len(password.encode()) > 72:
		logger.warning("Password exceeds 72 bytes, truncating for bcrypt")
		password = password[:72]
	
	salt = bcrypt.gensalt(rounds=PASSWORD_HASH_ROUNDS)
	hashed = bcrypt.hashpw(password.encode(), salt)
	return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""
	Verify plain password against stored hashed password.
	
	Args:
		plain_password: Plain text password from login
		hashed_password: Stored hashed password from database
		
	Returns:
		True if password matches, False otherwise
	"""
	if len(plain_password.encode()) > 72:
		plain_password = plain_password[:72]
	
	try:
		return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
	except Exception as exc:
		logger.error("Password verification error: %s", exc)
		return False


def create_access_token(
	data: dict,
	expiresedelta: Optional[timedelta] = None,
) -> str:
	"""
	Create JWT access token with expiration.
	
	Args:
		data: Payload dictionary to encode (e.g., {"sub": user_email})
		expiresedelta: Optional custom expiration time
		
	Returns:
		Encoded JWT token string
	"""
	to_encode = data.copy()
	if expiresedelta:
		expire = datetime.utcnow() + expiresedelta
	else:
		expire = datetime.utcnow() + timedelta(
			minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
		)
	to_encode.update({"exp": expire})

	try:
		encoded_jwt = jwt.encode(
			to_encode,
			settings.JWT_SECRET_KEY,
			algorithm=settings.JWT_ALGORITHM,
		)
		logger.debug("JWT token created successfully for subject: %s", data.get("sub"))
		return encoded_jwt
	except Exception as exc:
		logger.exception("Error creating JWT token: %s", exc)
		raise ValueError("Failed to create access token") from exc


def verify_access_token(token: str) -> dict:
	"""
	Verify and decode JWT access token.
	
	Args:
		token: JWT token string to verify
		
	Returns:
		Decoded token payload as dictionary
		
	Raises:
		ValueError: If token is invalid, expired, or malformed
	"""
	try:
		payload = jwt.decode(
			token,
			settings.JWT_SECRET_KEY,
			algorithms=[settings.JWT_ALGORITHM],
		)
		logger.debug("JWT token verified successfully")
		return payload
	except JWTError as exc:
		logger.error("JWT verification failed: %s", str(exc))
		if "expired" in str(exc).lower():
			raise ValueError("Token has expired") from exc
		raise ValueError("Invalid or malformed token") from exc
	except Exception as exc:
		logger.exception("Unexpected error verifying token: %s", exc)
		raise ValueError("Token verification failed") from exc