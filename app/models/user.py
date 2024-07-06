import datetime
import typing

from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.models.base import BaseModel
from sqlalchemy.orm import validates, relationship
import enum
from app.models.mixins.user import UserRelationMixin
from app.core.config import SETTINGS
from utils import password as password_util

if typing.TYPE_CHECKING:
    from utils.utility import UTILITY


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

    MESSAGE = 'Sizning tasdiqlash kodingiz: %s'

    def send_confirmation_email(self):
        email = self.user.email if self.user else None

        assert email is not None, "Email must be set"

        UTILITY.send_code_email(email, self.MESSAGE % self.code)


class User(BaseModel):
    HASHED_PREFIX = '$2b$12$'

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

    def check_password(self, password: str):

        hashed_password_with_prefix = self.password[len(self.HASHED_PREFIX):]
        return password_util.verify_password(
            password,
            hashed_password_with_prefix.encode('utf-8'),
        )

    def set_password(self, password: str = None):

        password = password or self.password

        if not password.startswith(self.HASHED_PREFIX):
            self.password = password_util.hash_password(password).decode('utf-8')
        else:
            self.password = password
