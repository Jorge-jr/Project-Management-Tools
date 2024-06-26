from app.models.user_role import UserRole
from pydantic import BaseModel, EmailStr, ConfigDict
from .work_item import WorkItemResponse


class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    is_active: bool
    work_items: "list[WorkItemResponse]"

    class Config:
        from_attributes = True


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    name: str
    role: UserRole


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class Contributors(BaseModel):
    contributors: list[int] = []