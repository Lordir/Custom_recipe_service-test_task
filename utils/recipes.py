from models.database import database
from models.recipes import recipes
from schemas import recipes as recipe_schema


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
