import random
import string
import hashlib
from models.database import database
from models.users import users, tokens
from schemas import users as user_schema
from datetime import datetime
from sqlalchemy import and_


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


async def create_user(user: user_schema.UserCreate):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users.insert().values(
        username=user.username, hashed_password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}


async def create_user_token(user_id: int):
    query = (
        tokens.insert()
            .values(expires=datetime.now(), user_id=user_id)
            .returning(tokens.c.token, tokens.c.expires)
    )

    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    query = tokens.join(users).select().where(
        and_(
            tokens.c.token == token,
        )
    )
    return await database.fetch_one(query)