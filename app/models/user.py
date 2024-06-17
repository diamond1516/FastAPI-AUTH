from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.models.base import BaseModel


class User(BaseModel):
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)

