from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils import jwt
from app.models import user as user_models
from app.api.deps import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Union
from jwt.exceptions import InvalidTokenError, DecodeError

http_bearer = HTTPBearer()


async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    try:
        payload = await jwt.decode_jwt(credentials.credentials)
        return payload
    except (InvalidTokenError, DecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def get_current_user(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_db)
) -> Union[user_models.User, None]:
    result = await db.execute(select(user_models.User).filter(
        user_models.User.id == payload['sub'], user_models.User.username == payload['username']
    ))
    return result.scalars().first()





