import time
import jwt
from app.api import dependencies as deps
from app.core.config import settings
from app.core import security
from app.models.user import User
from app.schemas.user import RefreshTokenRequest, AccessTokenResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/access-token", response_model=AccessTokenResponse)
async def login_access_token(
        session: AsyncSession = Depends(deps.get_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return security.generate_access_token_response(str(user.id))


@router.post("/refresh-token", response_model=AccessTokenResponse)
async def refresh_token(
        input: RefreshTokenRequest,
        session: AsyncSession = Depends(deps.get_session),
):
    """OAuth2 compatible token, get an access token for future requests using refresh token"""
    try:
        payload = jwt.decode(
            input.refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == int(token_data.sub)))
    user = result.scalars().first()

    if user is None:
        print("not found!")
        raise HTTPException(status_code=404, detail="User not found")

    return security.generate_access_token_response(str(user.id))
