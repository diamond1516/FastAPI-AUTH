from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import auth
from app.models.user import User
from app.api.deps import get_db
from app.schemas.auth import UserSchema
from utils import password, jwt, validators, user_helper, utility
from typing import Union


api_router = APIRouter(prefix="/auth", tags=["auth"])


@api_router.post(
    "/signup/",
    response_model=auth.TokenSchema,
)
async def signup(
        user_data: auth.SignupSchema = Depends(validators.signup_validator),
        db: AsyncSession = Depends(get_db)
):
    data = user_data.dict()
    data["password"] = password.hash_password(user_data.password).decode("utf-8")

    new_user = User(**data)

    code = ...

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    payload = await utility.UTILITY.get_jwt_payload(new_user)
    token = await jwt.encode_jwt(payload)

    return auth.TokenSchema(access_token=token)


@api_router.post(
    '/login/',
    response_model=auth.TokenSchema,
)
async def login(
        user: User = Depends(validators.login_validator),
        db: AsyncSession = Depends(get_db),
):

    user.last_login = datetime.utcnow()

    db.add(user)
    await db.commit()
    await db.refresh(user)

    payload = await utility.UTILITY.get_jwt_payload(user)

    token = await jwt.encode_jwt(payload)
    return auth.TokenSchema(access_token=token)


async def get_user_schema(
        user: Union[User, None] = Depends(user_helper.get_current_user),
) -> auth.UserSchema:
    return UserSchema(
        **user.__dict__
    )


@api_router.get(
    '/user-me/',
    response_model=auth.UserSchema,
)
async def user_me(
        current_user: auth.UserSchema = Depends(get_user_schema)
):
    return current_user




