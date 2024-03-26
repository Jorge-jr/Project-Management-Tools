from app.api import dependencies as deps
from app.models.user import User
from app.models.user_role import UserRole
from app.models.work_item import *
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


@router.post("/set_parent_project/")
async def set_parent_project(
        complex_task_id: int,
        project_id: int,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    try:
        complex_task = await session.get(ComplexTask, complex_task_id)
        project = await session.get(Project, project_id)

        if current_user.role <= UserRole.ASSOCIATE and current_user.id != complex_task.driver_id:
            raise HTTPException(status_code=401, detail="Not authorized")

        if not project or not complex_task:
            raise HTTPException(status_code=404, detail="not found")

        complex_task.project_id = project_id
        await session.commit()
        return {"message": f"Done"}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="not found")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await session.close()
