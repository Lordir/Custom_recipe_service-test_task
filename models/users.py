import enum
import sqlalchemy
from sqlalchemy import MetaData, Column, Table, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

metadata = MetaData()


class MyEnum(enum.Enum):
    one = ""


users = Table("users", metadata,
              Column("id", Integer, primary_key=True),
              Column("username", String, unique=True, index=True),
              Column("hashed_password", String()),
              Column(
                  "is_active",
                  Boolean(),
                  server_default=sqlalchemy.sql.expression.true(),
                  nullable=False,
              ),
              Column("favorites", Enum(MyEnum)),
              Column("created_on", DateTime(timezone=True), server_default=func.now()),
              Column("updated_on", DateTime(timezone=True), onupdate=func.now()),

              )

tokens = Table("tokens", metadata,
               Column("id", Integer, primary_key=True),
               Column(
                   "token",
                   UUID(as_uuid=False),
                   server_default=sqlalchemy.text("uuid_generate_v4()"),
                   unique=True,
                   nullable=False,
                   index=True,
               ),
               Column("expires", DateTime()),
               Column("user_id", ForeignKey("users.id")),
               )
