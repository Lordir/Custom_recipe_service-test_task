from fastapi import APIRouter, HTTPException, Depends
from schemas import users
from utils import users as users_utils
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependecies import get_current_user, get_admin_user
from utils.users import get_recipe_list_user, get_list_top_user, block_users, unblock_users, block_recipes, \
    unblock_recipes, top_users_likes, change_usernames, delete_users
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


@router.post("/sign-up", response_model=users.User)
async def create_user(user: users.UserCreate):
    db_user = await users_utils.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await users_utils.create_user(user=user)


@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_username(username=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not users_utils.validate_password(
            password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return await users_utils.create_user_token(user_id=user["id"])


@router.get("/user_profile", response_model=users.UserProfile)
async def user_profile(token=Depends(oauth2_scheme)):
    user = await users_utils.get_user_by_token(token)
    recipe_list = await get_recipe_list_user(dict(user)['user_id'])
    data = dict(user)
    data['number_of_recipes'] = len(recipe_list)
    return data


@router.get("/top_users")
async def top_users(current_user: users.User = Depends(get_current_user)):
    users_list = await get_list_top_user()
    return users_list


@router.get("/top_users_likes")
async def top_users_like(current_user: users.User = Depends(get_current_user)):
    users_list = await top_users_likes()
    return users_list


@router.get("/top_users")
async def user_profile(current_user: users.User = Depends(get_current_user)):
    users_list = await get_list_top_user()
    return users_list


@router.get("/admin/block_user/{user_id}")
async def block_user(user_id: int, current_user: users.User = Depends(get_admin_user)):
    user = await block_users(user_id)
    return user


@router.get("/admin/unblock_user/{user_id}")
async def unblock_user(user_id: int, current_user: users.User = Depends(get_admin_user)):
    user = await unblock_users(user_id)
    return user


@router.get("/admin/block_recipe/{recipe_id}")
async def block_recipe(recipe_id: int, current_user: users.User = Depends(get_admin_user)):
    recipe = await block_recipes(recipe_id)
    return recipe


@router.get("/admin/unblock_recipe/{recipe_id}")
async def unblock_recipe(recipe_id: int, current_user: users.User = Depends(get_admin_user)):
    recipe = await unblock_recipes(recipe_id)
    return recipe


@router.post("/change_username/{new_username}")
async def change_username(new_username: str, current_user: users.User = Depends(get_current_user)):
    user = await change_usernames(new_username, dict(current_user)['user_id'])
    return user


@router.get("/delete_user")
async def delete_user(current_user: users.User = Depends(get_current_user)):
    recipe = await delete_users(dict(current_user)['user_id'])
    return recipe
