from app.core.routes import Routes
from app.api.views import auth
from app.api.websockets import ws

__routes__ = Routes(routers=(auth.api_router, ws.router))
