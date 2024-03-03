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
    owner: dict

class WorkItemCreate(WorkItemBase):
    pass

class WorkItem(WorkItemBase):
    id: int

    class Config:
        orm_mode = True


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class WorkItemResponse(BaseResponse):
    id: int
    title: str
    # owner_id: Optional[User]
