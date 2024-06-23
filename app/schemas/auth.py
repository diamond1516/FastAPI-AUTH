from pydantic import BaseModel


class SignupSchema(BaseModel):
    username: str
    email: str = None
    password: str
    first_name: str = None


class LoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
