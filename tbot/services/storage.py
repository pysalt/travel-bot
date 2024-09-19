from aiogram.fsm.storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient


def get_storage(host: str, port: int, username: str, password: str) -> MongoStorage:
    client = AsyncIOMotorClient(host=host, port=port, username=username, password=password)
    return MongoStorage(client=client)
