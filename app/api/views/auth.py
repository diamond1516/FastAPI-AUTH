from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api import validators

from app.schemas import auth
from app.models.user import User
from app.api.deps import get_db
from utils import password, jwt


async def get_jwt_payload(user: User) -> dict:
    user_data = user.__dict__
    return dict(
        sub=user_data['id'],
        username=user_data['username'],
    )


api_router = APIRouter(prefix="/auth", tags=["auth"])


@api_router.post(
    "/signup/",
    response_model=auth.TokenSchema
)
async def signup(
        user_data: auth.SignupSchema = Depends(validators.signup_validator),
        db: AsyncSession = Depends(get_db)
):
    data = user_data.dict()
    data["password"] = password.hash_password(user_data.password).decode("utf-8")

    new_user = User(**data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    payload = await get_jwt_payload(new_user)
    token = await jwt.encode_jwt(payload)

    return auth.TokenSchema(access_token=token)


@api_router.post(
    '/login/',
    response_model=auth.TokenSchema
)
async def login(
        data: auth.LoginSchema = Depends(validators.login_validator),
):
    payload = {
        'id': data.id,
        'username': data.username,
    }

    token = await jwt.encode_jwt(payload)
    return auth.TokenSchema(access_token=token)
