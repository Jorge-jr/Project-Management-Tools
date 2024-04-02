from datetime import datetime
from app.api import dependencies as deps
from app.models.work_item_factory import *
from app.schemas.work_item import WorkItemCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.work_item import WorkItem
from app.models.user import User

router = APIRouter()

WORK_ITEM_SUBCLASSES = {
    WorkItemType.TASK: Task,
    WorkItemType.PROJECT: Project,
    WorkItemType.COMPLEX_TASK: ComplexTask
}


def prepare_work_item_response(item: WorkItem) -> dict:
    new_item = {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "due_date": item.due_date,
        "status": item.status,
        "contributors": [contributors.id for contributors in item.contributors],
        "initial_date": item.initial_date,
        "finished_date": item.finished_date,
        "driver_id": item.driver_id,
        "parent_id": item.get_parent_id(),
        "children_ids": item.get_children()
    }
    return new_item


@router.get("/work_item_list")
async def read_work_items(
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    result = await session.execute(select(WorkItem))
    work_items = result.scalars().unique().all()
    response = []

    for item in work_items:
        response.append(prepare_work_item_response(item))

    return response


@router.get("/{id}")
async def get_work_item(id: int, session: AsyncSession = Depends(deps.get_session)):

    work_item = await session.get(WorkItem, id)
    return prepare_work_item_response(work_item)


@router.post("/new_work_item")
async def create_work_item(
        work_item: WorkItemCreate,
        factory: WorkItemFactory = Depends(deps.get_work_item_factory),
        session: AsyncSession = Depends(deps.get_session),
):
    try:
        new_work_item_data = {key: value for key, value in work_item.dict().items() if
                              key not in ["parent", "contributors"]}
        new_work_item = await factory.create_work_item(new_work_item_data)

        if work_item.parent:
            parent = await session.get(WorkItem, work_item.dict()['parent'])
            if parent is None:
                raise ValueError(f"Parent with ID {work_item.dict()['parent']} not found")
            if parent.work_item_type == WorkItemType.PROJECT:
                new_work_item.project_id = parent.id
            elif parent.work_item_type == WorkItemType.COMPLEX_TASK:
                new_work_item.complex_task_id = parent.id
            else:
                raise ValueError("Invalid parent type.")

        session.add(new_work_item)
        await session.commit()

        return {"new_item_id": new_work_item.id, "message": "Successfully created a new work item"}
    except Exception as e:
        print(f"An error occurred: {e}")
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


@router.get("/set_due_date/{work_item_id}/")
async def set_due_date(
    new_due_date: datetime,
    work_item_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    work_item = await session.get(WorkItem, work_item_id)
    if not work_item:
        raise HTTPException(status_code=404, detail="Work item not found")

    if new_due_date < datetime.now():
        raise HTTPException(status_code=403, detail="Due date cannot be greater than current date")

    work_item.due_date = new_due_date
    await session.commit()

    return {"message": "Due date updated successfully"}


@router.get("/close_work_item/{work_item_id}/")
async def close_work_item(
        user_id: int,
        work_item_id: int,
        session: AsyncSession = Depends(deps.get_session),
        finished_date: datetime = datetime.utcnow()
):
    work_item = await session.get(WorkItem, work_item_id)
    user = await session.get(User, user_id)

    if not work_item:
        raise HTTPException(status_code=400, detail="Work item not found")

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    work_item.finished_date = finished_date
    await session.commit()
    return {"message": "Work item closed successfully"}
