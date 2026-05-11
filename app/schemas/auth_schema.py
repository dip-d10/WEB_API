"""
Authentication request and response schemas.

Defines Pydantic models for:
- User registration
- User login
- Token responses
- User profile responses
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
	"""Schema for user registration request.
	
	Fields:
	- name: User's full name
	- email: User's email address (must be valid)
	- password: User's password (minimum 8 characters)
	"""
	name: str = Field(..., min_length=1, max_length=255, description="User's full name")
	email: EmailStr = Field(..., description="User's email address")
	password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
	
	class Config:
		json_schema_extra = {
			"example": {
				"name": "John Doe",
				"email": "john@example.com",
				"password": "secure_password_123"
			}
		}


class LoginRequest(BaseModel):
	"""Schema for user login request.
	
	Fields:
	- email: User's email address (must be valid)
	- password: User's password
	"""
	email: EmailStr = Field(..., description="User's email address")
	password: str = Field(..., description="User's password")
	
	class Config:
		json_schema_extra = {
			"example": {
				"email": "john@example.com",
				"password": "secure_password_123"
			}
		}


class TokenResponse(BaseModel):
	"""Schema for JWT token response.
	
	Fields:
	- access_token: JWT token string
	- token_type: Type of token (always "bearer")
	"""
	access_token: str = Field(..., description="JWT access token")
	token_type: str = Field("bearer", description="Token type (always 'bearer')")
	
	class Config:
		json_schema_extra = {
			"example": {
				"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
				"token_type": "bearer"
			}
		}


class UserResponse(BaseModel):
	"""Schema for user profile response.
	
	Fields:
	- id: User's unique identifier
	- name: User's full name
	- email: User's email address
	"""
	id: str = Field(..., description="User's unique identifier")
	name: str = Field(..., description="User's full name")
	email: EmailStr = Field(..., description="User's email address")
	
	class Config:
		json_schema_extra = {
			"example": {
				"id": "507f1f77bcf86cd799439011",
				"name": "John Doe",
				"email": "john@example.com"
			}
		}