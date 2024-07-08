from app.core.routes import Routes
from app.api.views import auth

__routes__ = Routes(routers=(auth.api_router,))

