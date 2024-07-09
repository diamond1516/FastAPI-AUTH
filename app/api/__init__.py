__all__ = (
    '__routes__',
)

from app.core.routes import Routes
from app.api.views import auth, api_test

__routes__ = Routes(routers=(auth.api_router, api_test.router))

