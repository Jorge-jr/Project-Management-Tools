from pydantic import BaseModel, EmailStr, ConfigDict


class WorkItemBase(BaseModel):
    title: str
    description: str | None = None


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