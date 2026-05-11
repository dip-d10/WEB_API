from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase

from app.core.config import settings


client: Optional[AsyncIOMotorClient] = None
database: Optional[AgnosticDatabase] = None


async def connect_to_mongo() -> None:
	global client, database

	try:
		client = AsyncIOMotorClient(settings.MONGO_URI)
		database = client[settings.MONGO_DB_NAME]
		await database.command("ping")
	except Exception as exc:
		raise


async def close_mongo_connection() -> None:
	global client

	if client is not None:
		client.close()
		client = None


def get_user_collection():
	if database is None:
		raise RuntimeError("MongoDB database is not initialized")
	return database["users"]


def get_prediction_collection():
	if database is None:
		raise RuntimeError("MongoDB database is not initialized")
	return database["prediction_history"]