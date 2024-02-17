from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class WorkItemBase(BaseModel):
    title: str
    description: str
    deadline: datetime = None
    initial_date: datetime = datetime.now()
    finished_date: datetime = None
    owner_id: int


class WorkItemCreate(WorkItemBase):
    pass

class WorkItem(WorkItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class WorkItemResponse(BaseResponse):
    id: int
    email: EmailStr