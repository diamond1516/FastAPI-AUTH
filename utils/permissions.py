from utils import BasePermission


class IsAuthenticated(BasePermission):

    async def has_permission(self, user, request, view=None):
        return user is not None
