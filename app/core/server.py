from fastapi import FastAPI
from app.api import routes as routes_api
from app.websocket import routes as websocket_routes
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import SETTINGS


async def on_startup() -> None:
    print('The app is working 🎊🎉🎛')


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)
        self.__register_events(app)
        self.__register_middlewares(app)
        self.__register_websocket(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def __register_routes(app):
        routes_api.__routes__.register_routes(app, prefix=SETTINGS.API_V1_STR)

    @staticmethod
    def __register_websocket(app: FastAPI):
        websocket_routes.__routes__.register_routes(app, prefix=SETTINGS.WEBSOCKET_PREFIX)

    @staticmethod
    def __register_events(app: FastAPI):
        app.on_event('startup')(on_startup)

    @staticmethod
    def __register_middlewares(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # yoki kerakli manbalarni kiriting
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
