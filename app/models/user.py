import datetime

from fastapi import HTTPException
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from app.models.base import BaseModel
from sqlalchemy.orm import validates, relationship
import enum
from app.models.mixins.user import UserRelationMixin
from app.core.config import SETTINGS


class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    NEW = 'new'


def default_expire_date():
    return datetime.datetime.utcnow() + SETTINGS.CODE_EXPIRE


class UserConfirmation(BaseModel, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = 'user_confirmation'

    code = Column(String(4), nullable=False)
    expire_date = Column(DateTime, nullable=False, default=default_expire_date)


class User(BaseModel):
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default=UserStatus.NEW.value)
    last_login = Column(DateTime(timezone=True), nullable=True, default=datetime.datetime.utcnow)

    user_confirmation = relationship("UserConfirmation", uselist=False, back_populates="user")

    @validates('status')
    def validate_status(self, key, status):
        if status not in [i.value for i in UserStatus]:
            raise HTTPException(status_code=400, detail='Invalid status')
        return status



