from datetime import datetime
from typing import List, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Item
from app.api.deps import get_db
from pydantic import BaseModel

router = APIRouter(
    prefix="/test",
    tags=["test"],
)

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


def get_pagination_params(
        page: int = Query(1, ge=1),
        page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)
):
    return {"page": page, "page_size": page_size}


class ItemSchema(BaseModel):
    id: int
    name: str
    created_at: datetime

    def dict(self, *args: Any, **kwargs: Any) -> dict:
        d = super().dict(*args, **kwargs)
        d['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return d

    def json(self, *args: Any, **kwargs: Any) -> dict:
        print(1111)
        return super().json(*args, **kwargs)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class PaginatedResponse(BaseModel):
    items: List[ItemSchema]
    total_items: int
    page: int
    page_size: int
    total_pages: int


@router.post(
    '/create-item/',
    response_model=PaginatedResponse,
)
async def create_item(
        data: ItemSchema,
        db: AsyncSession = Depends(get_db),
):
    for i in range(100):
        item = Item(**data.dict())
        db.add(item)
        await db.flush()
    await db.commit()
    return {'msg': 'Items created'}


@router.get("/items/")
async def get_items(
        pagination: dict = Depends(get_pagination_params),
        db: AsyncSession = Depends(get_db)
):
    page = pagination['page']
    page_size = pagination['page_size']

    # Ma'lumotlar bazasidagi umumiy elementlar sonini aniqlash
    total_items = await db.scalar(select(func.count()).select_from(Item))

    # Paginatsiya qilingan ma'lumotlarni olish
    offset = (page - 1) * page_size
    items_query = select(Item).offset(offset).limit(page_size)
    items = await db.execute(items_query)
    items = items.scalars().all()

    # Paginatsiya natijalarini qaytarish

    return PaginatedResponse(
        items=items,
        total_items=total_items,
        page=page,
        page_size=page_size,
        total_pages=(total_items + page_size - 1) // page_size
    )

    # return {
    #     "items": items,
    #     "total_items": total_items,
    #     "page": page,
    #     "page_size": page_size,
    #     "total_pages": (total_items + page_size - 1) // page_size
    # }
