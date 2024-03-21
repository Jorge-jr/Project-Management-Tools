from typing import List
from app.api import dependencies as deps
from app.models.team import Team
from app.models.user import User
from app.models.user import user_team_association
from app.models.work_item import *
from app.models.work_item_enums import WorkItemType
from app.models.work_item_factory import *
from app.schemas.work_item import WorkItemCreate, WorkItemBase
from app.schemas.user import Contributors
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

WORK_ITEM_SUBCLASSES = {
    WorkItemType.TASK: Task,
    WorkItemType.EPIC: Epic,
    WorkItemType.FEATURE: Feature
}


@router.get("/work_item_list", response_model=List[WorkItemBase])
async def read_work_items(
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    result = await session.execute(select(WorkItem))
    work_items = result.scalars().unique().all()
    return work_items


@router.get("/{id}")
async def get_work_item(id: int, session: AsyncSession = Depends(deps.get_session)):
    work_item = await session.get(WorkItem, id)

    work_item_type_class = WORK_ITEM_SUBCLASSES[work_item.type]

    query = select(work_item_type_class, User, Team). \
        join(User, work_item_type_class.driver_id == User.id). \
        join(user_team_association, User.id == user_team_association.c.user_id). \
        join(Team, Team.id == user_team_association.c.team_id). \
        filter(work_item_type_class.id == id)

    query_result = await session.execute(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    item, driver, team = result
    parent_id = item.get_parent_id()
    children = item.get_children()

    return {"item": item, "driver": driver}


@router.post("/new_work_item")
async def create_work_item(
        work_item: WorkItemCreate,
        session: AsyncSession = Depends(deps.get_session),
):
    try:
        if work_item.type not in [WorkItemType.TASK, WorkItemType.EPIC, WorkItemType.FEATURE]:
            raise HTTPException(status_code=400, detail="Invalid work item type")

        if work_item.type == WorkItemType.TASK:
            factory = TaskFactory()
        elif work_item.type == WorkItemType.EPIC:
            factory = EpicFactory()
        elif work_item.type == WorkItemType.FEATURE:
            factory = FeatureFactory()

        new_work_item = factory.create_work_item(work_item.dict())

        session.add(new_work_item)
        await session.commit()

        return new_work_item
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")
        # Raise an HTTPException with status code 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while creating the work item")


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


@router.post("/{work_item_id}/contributors/")
async def add_contributors_to_work_item(
        work_item_id: int,
        contributor_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    work_item = await session.get(WorkItem, work_item_id)
    if not work_item:
        raise HTTPException(status_code=404, detail="Work item not found")

    user = await session.get(User, contributor_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    work_item.contributors.append(user)

    await session.commit()
    return {"message": "Contributors added successfully"}