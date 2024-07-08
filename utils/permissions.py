from utils import BasePermission
from fastapi import Request
from typing import Union
from app.models.user import User


class IsAuthenticated(BasePermission):

    async def has_permission(self, user: Union[User, None], request: Request, view=None):
        return user is not None
