"""
Run this script ONCE to create the manager and sample workers in MongoDB.
Usage:
    python seed_users.py
"""
import asyncio
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")


def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def seed():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.warehouse_db

    await db.users.delete_many({})

    users = [
        {
            "username": "manager1",
            "password_hash": hash_pw("manager123"),
            "role": "manager"
        },
        {
            "username": "worker1",
            "password_hash": hash_pw("worker123"),
            "role": "worker"
        },
        {
            "username": "worker2",
            "password_hash": hash_pw("worker123"),
            "role": "worker"
        }
    ]

    await db.users.insert_many(users)
    print("Users seeded successfully!")
    print("Manager  -> username: manager1  | password: manager123")
    print("Worker 1 -> username: worker1   | password: worker123")
    print("Worker 2 -> username: worker2   | password: worker123")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
