from fastapi import APIRouter, Depends, HTTPException

from app.schemas.work_item import WorkItemResponse

router = APIRouter()


@router.get("/work_items", response_model=WorkItemResponse)
def get_work_items():
    return {"message": "Hello World"}