from app.api import dependencies as deps
from app.models.user import User
from app.models.user_role import UserRole
from app.models.work_item import *
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


@router.post("/set_epic/")
async def set_parent_epic(
        feature_id: int,
        epic_id: int,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user_from_token)
):
    try:
        feature = await session.get(Feature, feature_id)
        epic = await session.get(Epic, epic_id)

        if current_user.role <= UserRole.ASSOCIATE and current_user.id != feature.driver_id:
            raise HTTPException(status_code=401, detail="Not authorized")

        if not epic or not feature:
            raise HTTPException(status_code=404, detail="not found")

        feature.epic_id = epic_id
        await session.commit()
        return {"message": f"Done"}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="not found")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await session.close()
