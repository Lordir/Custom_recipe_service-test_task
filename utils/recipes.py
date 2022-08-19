from models.database import database
from models.recipes import recipes
from schemas import recipes as recipe_schema
from operator import itemgetter
from fastapi import HTTPException, status
from sqlalchemy.sql import func


async def add_recipes(recipe: recipe_schema.RecipeModel, user):
    query = (
        recipes.insert()
            .values(
            title=recipe.title,
            type_dish=recipe.type_dish,
            description=recipe.description,
            cooking_steps=recipe.cooking_steps,
            photo=recipe.photo,
            likes=0,
            user_id=user["user_id"],
        )
    )
    recipe_id = await database.fetch_one(query)
    id_r = dict(zip(recipe_id, recipe_id.values()))
    return {"id": id_r['id'], "user": user["username"], **recipe.dict()}


async def get_recipes(recipe_id: int):
    recipe_list = await database.fetch_all(query=recipes.select().where(recipes.c.id == recipe_id))
    return [dict(result) for result in recipe_list]


async def like_recipes(recipe_id: int):
    recipe_list = await database.fetch_all(query=recipes.select().where(recipes.c.id == recipe_id))
    recipe_list = [dict(result) for result in recipe_list]
    for i in recipe_list:
        i['likes'] += 1
        i['updated_on'] = func.now()
    recipe_new = recipes.update().where(recipes.c.id == recipe_id).values(*recipe_list)
    g = await database.execute(recipe_new)
    return recipe_list


async def get_list_recipes():
    get_data = await database.fetch_all(query=recipes.select().where(recipes.c.is_active == True))
    recipes_list = [dict(result) for result in get_data]
    list_keys = [key for key in recipes_list[0].keys()]
    list_keys.pop(7)
    recipes_list_without_cooking_steps = [
        {key: value for key, value in item.items() if key in list_keys} for
        item
        in recipes_list]
    return recipes_list_without_cooking_steps


async def get_list_recipes_with_pagination(number: int):
    if number < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only positive number",
        )
    recipes_list = await get_list_recipes()
    if (number - 1) * 10 > len(recipes_list):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Page does not exist",
        )
    else:
        recipes_list_new = recipes_list[(number - 1) * 10:number * 10]
        return recipes_list_new


async def get_list_recipes_sort_likes():
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('likes'), reverse=True)
    return recipes_list


async def get_list_recipes_sort_likes_with_pagination(number: int):
    if number < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only positive number",
        )
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('likes'), reverse=True)
    if (number - 1) * 10 > len(recipes_list):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Page does not exist",
        )
    else:
        recipes_list_new = recipes_list[(number - 1) * 10:number * 10]
        return recipes_list_new


async def get_list_recipes_sort_date():
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('created_on'), reverse=True)
    return recipes_list


async def get_list_recipes_sort_date_with_pagination(number: int):
    if number < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only positive number",
        )
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('created_on'), reverse=True)
    if (number - 1) * 10 > len(recipes_list):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Page does not exist",
        )
    else:
        recipes_list_new = recipes_list[(number - 1) * 10:number * 10]
        return recipes_list_new


async def get_list_recipes_sort_name():
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('title'))
    return recipes_list


async def get_list_recipes_sort_name_with_pagination(number: int):
    if number < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only positive number",
        )
    recipes_list = await get_list_recipes()
    recipes_list.sort(key=itemgetter('title'))
    if (number - 1) * 10 > len(recipes_list):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Page does not exist",
        )
    else:
        recipes_list_new = recipes_list[(number - 1) * 10:number * 10]
        return recipes_list_new
