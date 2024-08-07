__all__ = (
    'BasePermission',
    'get_user_with_permissions',
    'get_current_user',
    'hash_password',
    'verify_password',
    'encode_jwt',
    'decode_jwt',
    'UTILITY',
)

from fastapi import Depends, Request, HTTPException, status
from utils.user_helper import get_current_user
from utils.password import hash_password, verify_password
from utils.utility import UTILITY
from utils.jwt import encode_jwt, decode_jwt
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class BasePermission:
    """
    This is the base permission class that all permissions must inherit from.
    """

    async def has_permission(self, user: Union['User', None], request: Request, view=None):
        """
        >>> self.has_permission(user, request, view)
        """

        raise NotImplementedError


def get_user_with_permissions(*permissions: type(BasePermission)):
    async def permission_checker(
            request: Request,
            user=Depends(get_current_user),
    ) -> Union['User', None]:

        for permission in (permission() for permission in permissions):
            if not await permission.has_permission(user, request):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action"
                )
        return user  # return user

    return permission_checker
