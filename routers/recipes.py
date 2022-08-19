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


@router.get("/get_recipe/{recipe_id}")
async def get_recipe(recipe_id: int, current_user: User = Depends(get_current_user)):
    recipe = await get_recipes(recipe_id)
    return recipe


@router.get("/get_recipe/{recipe_id}/like")
async def like_recipe(recipe_id: int, current_user: User = Depends(get_current_user)):
    recipe = await like_recipes(recipe_id)
    return recipe


@router.get("/get_list_recipe")
async def get_list_recipe(current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes()
    return recipe_list


@router.get("/get_list_recipe/pagination/{number}")
async def get_list_recipe_with_pagination(number: int, current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_with_pagination(number)
    return recipe_list


@router.get("/get_list_recipe/sort_likes")
async def get_list_recipe_sort_likes(current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_likes()
    return recipe_list


@router.get("/get_list_recipe/sort_likes/{number}")
async def get_list_recipe_sort_likes_with_pagination(number: int, current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_likes_with_pagination(number)
    return recipe_list


@router.get("/get_list_recipe/sort_date")
async def get_list_recipe_sort_date(current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_date()
    return recipe_list


@router.get("/get_list_recipe/sort_date/{number}")
async def get_list_recipe_sort_date_with_pagination(number: int, current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_date_with_pagination(number)
    return recipe_list


@router.get("/get_list_recipe/sort_name")
async def get_list_recipe_sort_name(current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_name()
    return recipe_list


@router.get("/get_list_recipe/sort_name/{number}")
async def get_list_recipe_sort_name_with_pagination(number: int, current_user: User = Depends(get_current_user)):
    recipe_list = await get_list_recipes_sort_name_with_pagination(number)
    return recipe_list
