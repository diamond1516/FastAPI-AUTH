from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str = None
    password: bytes
    first_name: str = None
    last_name: str = None
