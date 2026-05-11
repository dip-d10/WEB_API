from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.dependencies.auth_dependency import get_current_user


@asynccontextmanager
async def lifespan(_: FastAPI):
	await connect_to_mongo()
	try:
		yield
	finally:
		await close_mongo_connection()


app = FastAPI(
	title=settings.APP_NAME,
	version=settings.APP_VERSION,
	debug=settings.DEBUG,
	lifespan=lifespan,
)


@app.get("/protected-test")
async def protected_test(current_user: dict = Depends(get_current_user)) -> dict:
	"""
	Temporary protected endpoint for testing authentication dependency.
	
	This endpoint demonstrates:
	- Token extraction from Authorization header
	- JWT validation
	- Authenticated user identification
	- Protected route access
	
	Args:
		current_user: Authenticated user info (injected by get_current_user dependency)
		
	Returns:
		JSON response with authenticated user information
	"""
	return {
		"message": "Authentication successful",
		"authenticated_user": current_user,
	}