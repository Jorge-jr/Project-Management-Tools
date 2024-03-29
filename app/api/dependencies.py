import time
from collections.abc import AsyncGenerator

import jwt
from app.core import security
from app.core.config import settings
from app.core.session import async_session
from app.models.user import User
from app.models.work_item_enums import WorkItemType
from app.models.work_item_factory import WorkItemFactory, TaskFactory, ProjectFactory, ComplexTaskFactory
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user_from_token(
        session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials -> {e}.",
        )
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials, token expired or not yet valid -> {token_data.expires_at}",
        )

    result = await session.execute(select(User).where(User.id == int(token_data.sub)))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def get_work_item_factory(work_item_type: WorkItemType) -> WorkItemFactory:
    if work_item_type == WorkItemType.TASK:
        return TaskFactory()
    elif work_item_type == WorkItemType.PROJECT:
        return ProjectFactory()
    elif work_item_type == WorkItemType.COMPLEX_TASK:
        return ComplexTaskFactory()
    else:
        raise HTTPException(status_code=400, detail="Invalid work item type")
