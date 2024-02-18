from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import dependencies as deps

from app.schemas.work_item import WorkItemResponse, WorkItemCreate, WorkItemBase
from app.models.work_item import WorkItem

router = APIRouter()


@router.get("/work_item_list", response_model=list[WorkItemResponse])
async def read_work_items(session: AsyncSession = Depends(deps.get_session)):
    async with session.begin():
        query = select(WorkItem)
        result = await session.execute(query)
        work_items = result.scalars().all()
        return work_items

@router.post("/new_work_item")
async def create_work_item(
        work_item: WorkItemBase,
        session: AsyncSession = Depends(deps.get_session),
):
    new_work_item = WorkItem(**work_item.dict())
    session.add(new_work_item)
    await session.commit()
    return work_item

@router.post("/delete/{id}")
async def delete_work_item(
        work_item_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    work_item = await session.get(WorkItem, work_item_id)
    if work_item:
        work_item.soft_delete()
        await session.commit()
        return {"message": f"work item {work_item.title} deleted"}
    return {"message": f"work item {work_item} does not exist"}