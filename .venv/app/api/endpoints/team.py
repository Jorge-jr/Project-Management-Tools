from fastapi import APIRouter, Depends, HTTPException
from app.schemas.team import TeamCreateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import dependencies as deps
from app.models.user import User
from app.models.user_role import UserRole
from sqlalchemy import select
from app.models.team import Team


router = APIRouter()

@router.post("/new")
async def create_team(
        new_team_request: TeamCreateRequest,
        current_user: User = Depends(deps.get_current_user_from_token),
        session: AsyncSession = Depends(deps.get_session)
):

    manager = await session.get(User, new_team_request.manager_id)
    if not manager:
        return {"message": f"Manager not found"}
    if manager.role != UserRole.MANAGER:
        return {"message": f"Invalid manager role"}
    new_team = Team(id=new_team_request.id, name=new_team_request.name, manager_id=manager.id)
    session.add(new_team)
    await session.commit()

    return {"message": f"Successfully created team {new_team.name}"}

@router.get("/teams")
async def get_teams(
        current_user: User = Depends(deps.get_current_user_from_token),
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Team))
    teams = result.scalars().all()
    return teams

@router.get("/{id}")
async def get_team_by_id(
        id: int,
        current_user: User = Depends(deps.get_current_user_from_token),
        session: User = Depends(deps.get_session)
):
    team = await session.get(Team, id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team