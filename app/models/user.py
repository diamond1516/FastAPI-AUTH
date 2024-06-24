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
import alembic as op


class UserStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class User(BaseModel):
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    status = Column(
        Enum(UserStatus),
        nullable=True, default=UserStatus.active
    )
