from pydantic import BaseModel, Field
from typing import Any


class SignupSchema(BaseModel):
    username: str
    email: str = None
    password: str
    first_name: str = None


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        exclude_defaults = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserSchema(BaseModel):
    id: int
    username: str
    email: str = None
    first_name: str = None
    password: str
    status: Any = None
