from fastapi import APIRouter, HTTPException, Depends
from schemas.recipes import RecipeModel
from schemas.users import User
from utils.dependecies import get_current_user
from utils.recipes import *

router = APIRouter()


@router.post("/add_recipe", status_code=201)
async def add_recipe(recipe: RecipeModel, current_user: User = Depends(get_current_user)):
    recipe = await add_recipes(recipe, current_user)
    return recipe



