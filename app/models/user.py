from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum
)
from app.models.base import BaseModel
import enum


class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class User(BaseModel):
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    status = Column(
        Enum(UserStatus, create_type=True),
        nullable=True, default=UserStatus.ACTIVE
    )
