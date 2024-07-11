__all__ = (
    '__routes__',
)

from app.core import Routes
from app.api.views import api_test_router, auth_router

__routes__ = Routes(routers=(api_test_router, auth_router))

