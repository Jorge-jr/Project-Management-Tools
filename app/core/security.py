import time
from app.core.config import settings
from app.schemas.user import AccessTokenResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTTokenPayload(BaseModel):
    sub: str | int
    refresh: bool
    issued_at: int
    expires_at: int


def generate_access_token_response(subject: str | int):
    access_token, expires_at, issued_at = create_jwt_token(
        subject, settings.jwt_expire_minutes, refresh=False
    )
    refresh_token, refresh_expires_at, refresh_issued_at = create_jwt_token(
        subject, settings.jwt_expire_minutes, refresh=True
    )
    return AccessTokenResponse(
        token_type="Bearer",
        access_token=access_token,
        expires_at=expires_at,
        issued_at=issued_at,
        refresh_token=refresh_token,
        refresh_token_expires_at=refresh_expires_at,
        refresh_token_issued_at=refresh_issued_at,
    )


def create_jwt_token(subject: str | int, exp_secs: int, refresh: bool):

    issued_at = int(time.time())
    expires_at = issued_at + exp_secs

    to_encode: dict[str, int | str | bool] = {
        "issued_at": issued_at,
        "expires_at": expires_at,
        "sub": subject,
        "refresh": refresh,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt, expires_at, issued_at


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
