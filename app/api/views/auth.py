from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user
from app.models.user import User
from app.api.deps import get_db
from utils import password, jwt

api_router = APIRouter(prefix="/auth", tags=["auth"])


@api_router.post("/signup", response_model=user.Signup)
def signup(user_data: user.Signup, db: AsyncSession = Depends(get_db)):
    password = user_data.password

    new_user = User(**user_data.dict())

    return new_user
