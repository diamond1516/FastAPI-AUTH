from fastapi import FastAPI
from app.core import Server, SETTINGS


def app() -> FastAPI:
    main = FastAPI(
        title=SETTINGS.PROJECT_NAME,
        debug=SETTINGS.DEBUG,
        version=SETTINGS.VERSION,
    )
    return Server(main).get_app()

