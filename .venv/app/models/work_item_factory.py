from abc import ABC, abstractmethod

from app.models.work_item import Task, project, Feature
from app.models.work_item_enums import WorkItemType


class WorkItemFactory(ABC):
    @abstractmethod
    def create_work_item(self, work_item_data: dict):
        pass

    @classmethod
    def get_factory(cls, type: WorkItemType):
        if type == WorkItemType.TASK:
            return TaskFactory()
        elif type == WorkItemType.FEATURE:
            return FeatureFactory()
        elif type == WorkItemType.project:
            return projectFactory()
        else:
            raise ValueError(f"Not valid a work_item type")


class TaskFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return Task(**work_item_data)


class projectFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return project(**work_item_data)


class FeatureFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return Feature(**work_item_data)
