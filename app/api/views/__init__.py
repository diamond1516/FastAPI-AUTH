__all__ = (
    'auth_router',
    'api_test_router',
)

from .auth import router as auth_router
from .api_test import router as api_test_router
