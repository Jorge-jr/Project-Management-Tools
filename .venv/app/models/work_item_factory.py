from abc import ABC, abstractmethod
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.work_item import Task, Project, ComplexTask, WorkItem
from app.models.user import User
from app.models.work_item_enums import WorkItemType
from sqlalchemy import select
from typing import Optional


class WorkItemFactory(ABC):
    @abstractmethod
    def create_work_item(self, work_item_data: Dict, session: AsyncSession):
        pass

    @classmethod
    def get_factory(cls, type: WorkItemType):
        if type == WorkItemType.TASK:
            return TaskFactory()
        elif type == WorkItemType.COMPLEX_TASK:
            return ComplexTaskFactory()
        elif type == WorkItemType.PROJECT:
            return ProjectFactory()
        else:
            raise ValueError(f"Not valid a work_item type")


class TaskFactory(WorkItemFactory):
    async def create_work_item(self, work_item_data: Dict):
        new_task = Task(**work_item_data)
        return new_task


class ProjectFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: Dict):
        new_project = Project(**work_item_data)

        return new_project


class ComplexTaskFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: Dict):
        new_complex_task = ComplexTask(**work_item_data)

        return new_complex_task