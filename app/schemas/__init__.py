"""
Schemas package - Contains Pydantic models for request/response validation.

Exports:
- Authentication schemas: RegisterRequest, LoginRequest, TokenResponse, UserResponse
- Prediction schemas: PredictionRequest, PredictionResponse, PredictionHistoryResponse
"""

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

__all__ = [
	# Auth schemas
	"RegisterRequest",
	"LoginRequest",
	"TokenResponse",
	"UserResponse",
	# Prediction schemas
	"PredictionRequest",
	"PredictionResponse",
	"PredictionHistoryResponse",
]
