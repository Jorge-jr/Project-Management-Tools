from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies as deps
from app.core.security import get_password_hash
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.user import UserCreateRequest, UserUpdatePasswordRequest, UserResponse


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


@router.post("/me/work_items")
async def get_user_work_items(
    current_user: User = Depends(deps.get_current_user_from_token),
    session: AsyncSession = Depends(deps.get_session)
):

    return current_user.work_items

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

@router.get("/{id}")
async def get_user(
        id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    user = await session.get(User, id)
    return {
        "email": user.email,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "teams": {team.id: team.name for team in user.teams},
        "work_items": {work_item.id: work_item.title for work_item in user.work_items},
        "full_name": user.full_name
    }