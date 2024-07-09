from app.models import BaseModel
from sqlalchemy import Column, Integer, String


class Item(BaseModel):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
