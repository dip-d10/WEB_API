from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.logger import get_logger


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
	logger.info("Application startup: initializing resources")
	await connect_to_mongo()
	try:
		yield
	finally:
		await close_mongo_connection()
		logger.info("Application shutdown: resources released")


app = FastAPI(
	title=settings.APP_NAME,
	version=settings.APP_VERSION,
	debug=settings.DEBUG,
	lifespan=lifespan,
)