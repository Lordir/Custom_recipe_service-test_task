import random
import string
import hashlib
from models.database import database
from models.users import users, tokens
from schemas import users as user_schema
from datetime import datetime
from sqlalchemy import and_
from models.recipes import recipes


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


async def get_recipe_list_user(user_id: int):
    recipe_list = await database.fetch_all(query=recipes.select().where(recipes.c.user_id == user_id))
    return [dict(result) for result in recipe_list]


async def get_list_top_user():
    get_data = await database.fetch_all(query=users.select().where(users.c.is_active == True))
    users_list = [dict(result) for result in get_data]
    print(users_list)
    users_dict = {}
    for user in users_list:
        user_id = user['id']
        number_of_recipes = await get_recipe_list_user(user_id)
        users_dict[user_id] = {
            'user_id': user['id'],
            'username': user['username'],
            'is_active': user['is_active'],
            'number_of_recipes': len(number_of_recipes)
        }
    sorted_tuples = sorted(users_dict.items(), key=lambda item: item[1]['number_of_recipes'], reverse=True)
    sorted_users_dict = {key: value for key, value in sorted_tuples}
    final_list = []
    if len(sorted_users_dict) < 10:
        i = len(sorted_users_dict)
    else:
        i = 10
    for user_id, user in sorted_users_dict.items():
        if i == 0:
            break
        else:
            final_list.append(user)
            i -= 1

    return final_list
