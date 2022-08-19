from fastapi import APIRouter, HTTPException, Depends
from schemas import users
from utils import users as users_utils
from fastapi.security import OAuth2PasswordRequestForm
from utils.dependecies import get_current_user
from utils.users import get_recipe_list_user, get_list_top_user
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
async def user_profile(current_user: users.User = Depends(get_current_user)):
    users_list = await get_list_top_user()
    return users_list
