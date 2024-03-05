from abc import ABC, abstractmethod
from app.models.work_item import Task, Epic, Feature

class WorkItemFactory(ABC):
    @abstractmethod
    def create_work_item(self, work_item_data: dict):
        pass

class TaskFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return Task(**work_item_data)

class EpicFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return Epic(**work_item_data)

class FeatureFactory(WorkItemFactory):
    def create_work_item(self, work_item_data: dict):
        return Feature(**work_item_data)