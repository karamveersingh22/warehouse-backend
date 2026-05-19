from app.database.mongodb import get_db
from app.utils.security import verify_password, create_access_token


async def login_user(username: str, password: str):
    db = get_db()
    user = await db.users.find_one({"username": username})

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    token = create_access_token({
        "sub": username,
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }
