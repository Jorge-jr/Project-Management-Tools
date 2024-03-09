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
from app.models.work_item_factory import *
from app.models.work_item_enums import WorkItemStatus, WorkItemType


router = APIRouter()


@router.get("/work_item_list", response_model=List[WorkItemBase])
async def read_work_items(
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    result = await session.execute(select(WorkItem))
    work_items = result.scalars().all()
    return work_items


@router.get("/{id}", response_model=WorkItemResponse)
async def get_work_item(id: int, session: AsyncSession = Depends(deps.get_session)):

    query = select(WorkItem, User, Team).\
        join(User, WorkItem.owner_id == User.id).\
        join(user_team_association, User.id == user_team_association.c.user_id).\
        join(Team, Team.id == user_team_association.c.team_id).\
        filter(WorkItem.id == id)

    query_result = await session.execute(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    work_item, owner, team = result
    parent_data = {}

    if work_item.has_parents():
        parent = await session.get(WorkItem, work_item.get_parent_id())
        parent_data["parent_title"] = parent.title
        parent_data["parent_id"] = parent.id,
        parent_data["parent_initial_date"] = parent.initial_date,
        parent_data["parent_finished_date"] =  parent.finished_date,
        parent_data["parent_deadline"] = parent.deadline

    features, tasks = None, None

    if work_item.tasks:
        tasks = work_item.tasks

    if work_item.features:
        features = work_item.features

    return {
        "id": work_item.id,
        "title": work_item.title,
        "description": work_item.description,
        "deadline": work_item.deadline,
        "initial_date": work_item.initial_date,
        "finished_date": work_item.finished_date,
        "is_deleted": work_item.is_deleted,
        "owner_id": work_item.owner_id,
        "owner": {
            "id": owner.id,
            "email": owner.email,
            "teams": {team.id: team.name for team in owner.teams},
            "name": owner.name
        },
        "parent": parent_data
    }


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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound

@router.post("/set_parent/")
async def set_parent(
        work_item_id: int,
        parent_id: int,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    try:
        # Fetch the work item and parent
        work_item = await session.get(WorkItem, work_item_id)
        parent = await session.get(WorkItem, parent_id)

        if not work_item or not parent:
            raise HTTPException(status_code=404, detail="not found")

        if parent.type < work_item.type:
            raise HTTPException(status_code=400, detail="parent-child relation not allowed for this work items")

        if parent.type == WorkItemType.FEATURE:
            work_item.feature_id = parent_id
        elif parent.type == WorkItemType.EPIC:
            work_item.epic_id = parent_id


        # Commit the changes to the database
        await session.commit()
        print(work_item.parent)
        return {"message": f"work item {work_item.id} has been updated"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="not found")
    except Exception as e:
        # Rollback the transaction in case of any error
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
