"""
Prediction request and response schemas.

Defines Pydantic models for:
- Prediction requests (input features)
- Prediction responses (model output)
- Prediction history (stored predictions)
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
	"""Schema for prediction request.
	
	Defines input features for ML model prediction.
	
	Fields:
	- feature_1: First input feature (float)
	- feature_2: Second input feature (float)
	- feature_3: Third input feature (float)
	"""
	feature_1: float = Field(..., description="First input feature")
	feature_2: float = Field(..., description="Second input feature")
	feature_3: float = Field(..., description="Third input feature")
	
	class Config:
		json_schema_extra = {
			"example": {
				"feature_1": 0.5,
				"feature_2": 1.2,
				"feature_3": 2.3
			}
		}


class PredictionResponse(BaseModel):
	"""Schema for prediction response.
	
	Contains model prediction output and metadata.
	
	Fields:
	- prediction: Predicted value or class (string)
	- confidence: Confidence score (0-1, optional)
	- model_version: Version of the model used
	- timestamp: When the prediction was made
	"""
	prediction: str = Field(..., description="Model prediction result")
	confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score (0-1)")
	model_version: str = Field(..., description="Version of the model")
	timestamp: datetime = Field(..., description="Timestamp of prediction")
	
	class Config:
		json_schema_extra = {
			"example": {
				"prediction": "Class A",
				"confidence": 0.95,
				"model_version": "1.0.0",
				"timestamp": "2026-05-12T10:30:00Z"
			}
		}


class PredictionHistoryResponse(BaseModel):
	"""Schema for prediction history response.
	
	Represents a stored prediction record.
	
	Fields:
	- user_id: ID of the user who made prediction
	- input_features: Dictionary of input features used
	- prediction_result: The model's prediction
	- model_version: Version of model used
	- timestamp: When the prediction was made
	"""
	user_id: str = Field(..., description="User's unique identifier")
	input_features: Dict[str, Any] = Field(..., description="Input features used for prediction")
	prediction_result: str = Field(..., description="Model prediction result")
	model_version: str = Field(..., description="Version of the model")
	timestamp: datetime = Field(..., description="Timestamp of prediction")
	
	class Config:
		json_schema_extra = {
			"example": {
				"user_id": "507f1f77bcf86cd799439011",
				"input_features": {
					"feature_1": 0.5,
					"feature_2": 1.2,
					"feature_3": 2.3
				},
				"prediction_result": "Class A",
				"model_version": "1.0.0",
				"timestamp": "2026-05-12T10:30:00Z"
			}
		}