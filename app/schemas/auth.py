from typing import Optional

from pydantic import BaseModel, Field


class SignupSchema(BaseModel):
    username: str
    email: str = None
    password: str
    first_name: str = None


class LoginSchema(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

    class Config:
        orm_mode = True
        exclude_defaults = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
