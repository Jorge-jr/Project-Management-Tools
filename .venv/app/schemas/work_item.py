from datetime import datetime
from typing import Optional
from app.models.work_item import *
from pydantic import BaseModel, ConfigDict


class WorkItemBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime] = None
    initial_date: datetime = datetime.now()
    finished_date: Optional[datetime] = None
    is_deleted: bool = False
    driver_id: int
    work_item_type: WorkItemType
    contributors: list = []
    status: WorkItemStatus = WorkItemStatus.NEW


class WorkItemCreate(WorkItemBase):
    parent: Optional[int] = None


class WorkItemResponse(WorkItemBase):
    """    parent_id: Optional[int] = None
    complex_tasks: list[complex_task] = []
    tasks: list[Task] = []
    driver: dict"""
    id: int

    class Config:
        orm_mode = True


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
