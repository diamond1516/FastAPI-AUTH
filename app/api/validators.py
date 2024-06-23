from app.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Form, status
from sqlalchemy import select, or_
from app.models import user as user_models
from app.schemas import auth
from utils import password


async def signup_validator(
        user_data: auth.SignupSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(user_models.User).filter(
        or_(user_models.User.username == user_data.username, user_models.User.email == user_data.email)
    ))

    user = result.scalars().first()

    if user and user.username == user_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username already exists"
        )
    if user and user_data.email and user.email == user_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists"
        )

    return user_data


async def login_validator(
        data: auth.LoginSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(user_models.User).filter(user_models.User.username == data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    if not password.verify_password(data.password, user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    data.id = user.id
    return data
