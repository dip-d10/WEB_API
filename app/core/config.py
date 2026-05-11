from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.logger import get_logger


logger = get_logger(__name__)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
	APP_NAME: str
	APP_VERSION: str
	DEBUG: bool

	MONGO_URI: str
	MONGO_DB_NAME: str

	JWT_SECRET_KEY: str
	JWT_ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int

	AZURE_STORAGE_CONNECTION_STRING: str
	AZURE_CONTAINER_NAME: str
	AZURE_MODEL_PATH: str
	AZURE_METADATA_PATH: str

	model_config = SettingsConfigDict(
		env_file=str(ENV_FILE_PATH),
		env_file_encoding="utf-8",
	)


@lru_cache()
def get_settings() -> Settings:
	try:
		loaded_settings = Settings()
		logger.info("Application settings loaded successfully")
		return loaded_settings
	except Exception as exc:
		logger.exception("Failed to load application settings: %s", exc)
		raise


settings = get_settings()