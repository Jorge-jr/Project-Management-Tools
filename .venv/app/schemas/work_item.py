from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, timezone
from typing import Optional


class WorkItemBase(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime] = None
    initial_date: datetime = datetime.now()
    finished_date: Optional[datetime] = None
    is_deleted: bool = False
    owner_id: int


class WorkItemCreate(WorkItemBase):
    owner_id: int


class WorkItemResponse(WorkItemBase):
    title: str
    description: str
    deadline: Optional[datetime] = None
    initial_date: datetime = datetime.now()
    finished_date: Optional[datetime] = None
    is_deleted: bool = False
    owner: dict

    class Config:
        orm_mode = True


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

