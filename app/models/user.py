import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from app.models.base import BaseModel
import enum


class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    NEW = 'new'


class User(BaseModel):
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default=UserStatus.NEW.value)
    last_login = Column(DateTime(timezone=True), nullable=True, default=datetime.datetime.utcnow)




