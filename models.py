import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class MyEnum(enum.Enum):
    one = ""


class MyEnum2(enum.Enum):
    one = ""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    favorites = Column(Enum(MyEnum))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    recipes = relationship("Recipe", back_populates="author")


class Recipe(Base):
    __tablename__ = "recipes"

    author = relationship("User", back_populates="recipes")
    id = Column(Integer, primary_key=True, index=True, unique=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    title = Column(String, index=True)
    type_dish = Column(String, index=True)
    description = Column(Text, index=True)
    cooking_steps = Column(Text, index=True)
    photo = Column(String, index=True)
    likes = Column(Integer)
    hashtags = Column(Enum(MyEnum2))
    is_active = Column(Boolean, default=True)
