from pydantic import UUID4, BaseModel, validator, Field
from datetime import datetime
from typing import Optional


class RecipeModel(BaseModel):
    title: str
    type_dish: str
    description: str
    cooking_steps: str
    photo: str
    likes: int

