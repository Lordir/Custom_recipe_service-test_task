from pydantic import UUID4, BaseModel, validator, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class UserBase(BaseModel):
    id: int
    username: str


class User(UserBase):
    token: TokenBase = {}
