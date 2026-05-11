import asyncio

from app.db.mongodb import close_mongo_connection, connect_to_mongo


async def main() -> None:
    await connect_to_mongo()
    await close_mongo_connection()
    print("MONGO_LIFECYCLE_OK")


if __name__ == "__main__":
    asyncio.run(main())
