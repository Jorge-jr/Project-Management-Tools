from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import dependencies as deps

from app.schemas.work_item import WorkItemResponse, WorkItemCreate, WorkItemBase
from app.models.work_item import WorkItem

router = APIRouter()


@router.get("/work_items/")
async def read_work_items(session: AsyncSession = Depends(deps.get_session)):
    async with session.begin():
        query = select(WorkItem)
        result = await session.execute(query)
        work_items = result.scalars().all()
        return work_items

@router.post("/work_item")
async def create_work_item(
        work_item: WorkItemBase,
        session: AsyncSession = Depends(deps.get_session),
):
    new_work_item = WorkItem(**work_item.dict())
    session.add(new_work_item)
    await session.commit()
    return work_item
