"""
Authentication dependencies for FastAPI.

This module provides reusable FastAPI dependencies for:
- Extracting JWT tokens from request headers
- Validating tokens
- Identifying current authenticated user
- Protecting private routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_access_token


# OAuth2 scheme to extract Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
	"""
	FastAPI dependency to extract and validate JWT token, returning authenticated user info.
	
	This dependency:
	1. Extracts Bearer token from Authorization header
	2. Verifies JWT token signature and expiration
	3. Decodes token payload
	4. Extracts user identity from "sub" field
	5. Returns authenticated user information
	
	Args:
		token: JWT token extracted from Authorization header by OAuth2PasswordBearer
		
	Returns:
		Dictionary containing:
		{
			"email": str  # User's email from token "sub" field
		}
		
	Raises:
		HTTPException: 401 Unauthorized if:
		- Token is missing
		- Token is invalid/malformed
		- Token is expired
		- Payload doesn't contain "sub" field
	"""
	try:
		# Verify token and decode payload
		payload = verify_access_token(token)
		
		# Extract user email from "sub" field
		user_email: str = payload.get("sub")
		if not user_email:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token: missing user identifier",
				headers={"WWW-Authenticate": "Bearer"},
			)
		
		return {"email": user_email}
		
	except ValueError as exc:
		# Token validation failed (invalid, expired, or malformed)
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=str(exc),
			headers={"WWW-Authenticate": "Bearer"},
		) from exc
	except Exception as exc:
		# Unexpected error during token processing
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Authentication failed",
			headers={"WWW-Authenticate": "Bearer"},
		) from exc