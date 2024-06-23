from fastapi import Depends, Request, HTTPException, status
from utils.user_helper import get_current_user


class BasePermission:
    async def has_permission(self, user, request, view=None):
        raise NotImplementedError


async def check_permission(permission: BasePermission):
    async def permission_checker(
            user=Depends(get_current_user),
            request: Request = Depends(),
    ):
        if not permission.has_permission(user, request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action"
            )

    return permission_checker
