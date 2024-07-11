__all__ = (
    '__routes__',
)

from app.core.routes import Routes
from app.websocket.consumers import ws_router


__routes__ = Routes(routers=(ws_router,))
