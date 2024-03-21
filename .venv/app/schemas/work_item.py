from datetime import datetime
from typing import Optional
from app.models.work_item import *
from pydantic import BaseModel, ConfigDict


class WorkItemBase(BaseModel):
    id: int
    title: str
    description: str
    due_date: Optional[datetime] = None
    initial_date: datetime = datetime.now()
    finished_date: Optional[datetime] = None
    is_deleted: bool = False
    driver_id: int
    type: WorkItemType
    status: WorkItemStatus = WorkItemStatus.NEW
    contributors: list[int] = []


class WorkItemCreate(WorkItemBase):
    driver_id: int


class WorkItemResponse(WorkItemBase):
    """    parent_id: Optional[int] = None
    features: list[Feature] = []
    tasks: list[Task] = []
    driver: dict"""
    pass

    class Config:
        orm_mode = True


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
