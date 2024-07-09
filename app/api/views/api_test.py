from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Item
from app.api.deps import get_db
from pydantic import BaseModel

router = APIRouter(
    prefix="/test",
    tags=["test"],
)

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


def get_pagination_params(page: int = Query(1, ge=1),
                          page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)):
    return {"page": page, "page_size": page_size}


class ItemSchema(BaseModel):
    name: str
    description: str


async def salom():
    return "salom"


@router.post('/create-item/')
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
    items_query = select(Item).with_only_columns(Item.id).offset(offset).limit(page_size)
    items = await db.execute(items_query)
    items = items.scalars().all()

    print(items)

    # Paginatsiya natijalarini qaytarish
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_items + page_size - 1) // page_size
    }
