from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import dependencies as deps
from typing import List
from app.schemas.work_item import WorkItemResponse, WorkItemCreate, WorkItemBase
from app.models.work_item import WorkItem
from app.models.user import User
from app.models.team import Team
from app.models.user import user_team_association


router = APIRouter()


@router.get("/work_item_list", response_model=List[WorkItemBase])
async def read_work_items(session: AsyncSession = Depends(deps.get_session)):
    async with session.begin():
        query = select(WorkItem)
        result = await session.execute(query)
        work_items = result.scalars().all()
        return work_items

@router.get("/{id}", response_model=WorkItemBase)
async def read_work_item(id: int, session: AsyncSession = Depends(deps.get_session)):
    query = select(WorkItem, User, Team).\
        join(User, WorkItem.owner_id == User.id).\
        join(user_team_association, User.id == user_team_association.c.user_id).\
        join(Team, Team.id == user_team_association.c.team_id).\
        filter(WorkItem.id == id)

    # Execute the query
    result = await session.execute(query)

    # Fetch the first result
    work_item, owner, team = result.first()
    return {
        "title": work_item.title,
        "description": work_item.description,
        "deadline": work_item.deadline,
        "initial_date": work_item.initial_date,
        "finished_date": work_item.finished_date,
        "is_deleted": work_item.is_deleted,
        "owner": {
            "id": owner.id,
            "email": owner.email,
            "teams": {team.id: team.name for team in owner.teams},
            "name": owner.name
        }
    }

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
