from pydantic import BaseModel


class SignupSchema(BaseModel):
    username: str
    email: str = None
    password: str
    first_name: str = None


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
