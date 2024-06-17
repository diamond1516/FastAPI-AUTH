from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
    "/signup",
    response_model=auth.Token
)
async def signup(user_data: auth.Signup, db: AsyncSession = Depends(get_db)):
    data = user_data.dict()
    data["password"] = password.hash_password(user_data.password).decode("utf-8")

    new_user = User(**data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    payload = await get_jwt_payload(new_user)
    token = await jwt.encode_jwt(payload)

    return auth.Token(access_token=token, )
