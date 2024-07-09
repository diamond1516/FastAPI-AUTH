__all__ = (
    '__routes__',
)

from app.core.routes import Routes
from app.websocket.consumers import ws


__routes__ = Routes(routers=(ws.router,))
