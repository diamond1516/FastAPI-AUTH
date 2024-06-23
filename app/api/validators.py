from app.api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Form, status
from sqlalchemy import select, or_
from app.models import user as user_models
from app.schemas import auth


async def signup_validator(
        user_data: auth.SignupSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(user_models.User).filter(
        or_(user_models.User.username == user_data.username, user_models.User.email == user_data.email)
    ))

    existing_user = result.scalars().first()

    if existing_user.username == user_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username already exists"
        )
    if user_data.email and existing_user.email == user_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists"
        )

    return user_data
