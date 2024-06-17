from pydantic import BaseModel


class Signup(BaseModel):
    username: str
    email: str = None
    password: str

