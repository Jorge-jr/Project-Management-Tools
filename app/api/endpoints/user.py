from app.api import dependencies as deps
from app.core.security import get_password_hash
from app.models.user import User
from app.models.work_item import *
from app.models.work_item_enums import WorkItemType
from app.schemas.user import UserCreateRequest, UserUpdatePasswordRequest, UserResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
        current_user: User = Depends(deps.get_current_user_from_token),
):
    return current_user


@router.delete("/me", status_code=204)
async def delete_current_user(
        current_user: User = Depends(deps.get_current_user_from_token),
        session: AsyncSession = Depends(deps.get_session),
):
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()


@router.get("/me/work_items")
async def get_user_work_items(
        current_user: User = Depends(deps.get_current_user_from_token),
        session: AsyncSession = Depends(deps.get_session)
):
    projects = filter(lambda item: item.type == WorkItemType.PROJECT, current_user.work_items)
    tasks = filter(lambda item: item.type == WorkItemType.TASK, current_user.work_items)
    complex_tasks = filter(lambda item: item.type == WorkItemType.COMPLEX_TASK, current_user.work_items)

    projects_list = [await session.get(project, project.id) for project in projects]
    complex_tasks_list = [await session.get(complex_task, complex_task.id) for complex_task in complex_tasks]
    tasks_list = [await session.get(Task, task.id) for task in tasks]

    items = {"projects": projects_list, "complex_tasks": complex_tasks_list, "tasks": tasks_list}

    return {"items": items, "user_name": current_user.name}


@router.post("/reset-password", response_model=UserResponse)
async def reset_current_user_password(
        user_update_password: UserUpdatePasswordRequest,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token),
):
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return current_user


@router.post("/register", response_model=UserResponse)
async def register_new_user(
        new_user: UserCreateRequest,
        session: AsyncSession = Depends(deps.get_session),
):
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        name=new_user.name,
        role=new_user.role
    )
    session.add(user)
    await session.commit()
    return user


@router.post("/delete/{user_id}")
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    user = await session.get(User, user_id)
    if user:
        user.soft_delete()
        await session.commit()
        return {"message": f"User {user.name} deleted"}


@router.get("/{user_id}")
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    user = await session.get(User, user_id)
    return {
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "teams": {team.id: team.name for team in user.teams},
        "work_items": {work_item.id: work_item.title for work_item in user.work_items},
        "full_name": user.full_name
    }


@router.post("/{id}/work_items")
async def get_user_work_items(
        id: int,
        current_user: User = Depends(deps.get_current_user_from_token),
        session: AsyncSession = Depends(deps.get_session)
):
    user = await session.get(User, id)
    return current_user.work_items
