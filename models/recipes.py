import enum
import sqlalchemy
from sqlalchemy import MetaData, Column, Table, Integer, String, Boolean, Enum, DateTime, ForeignKey, Text
from datetime import datetime
from models.users import users

metadata = MetaData()


class MyEnum2(enum.Enum):
    one = ""


recipes = Table("recipes", metadata,
                Column("id", Integer, primary_key=True),
                Column("user_id", ForeignKey(users.c.id)),
                Column("created_on", DateTime(), default=datetime.now),
                Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now),
                Column("title", String, index=True),
                Column("type_dish", String, index=True),
                Column("description", Text, index=True),
                Column("cooking_steps", Text, index=True),
                Column("photo", String, index=True),
                Column("likes", Integer),
                Column("hashtags", Enum(MyEnum2)),
                Column(
                    "is_active",
                    Boolean(),
                    server_default=sqlalchemy.sql.expression.true(),
                    nullable=False,
                )
                )
