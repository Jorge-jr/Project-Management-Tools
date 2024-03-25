from app.db.database import Base
from app.models.work_item_enums import WorkItemStatus, WorkItemType
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models.work_items_contributors import work_item_contributors


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    due_date = Column(DateTime, index=True)
    initial_date = Column(DateTime, index=True)
    finished_date = Column(DateTime, index=True)
    is_deleted = Column(Boolean, default=False)
    status = Column(Enum(WorkItemStatus), default=WorkItemStatus.NEW)
    work_item_type = Column(Enum(WorkItemType), default=WorkItemType.TASK)
    driver_id = Column(Integer, ForeignKey("users.id"))

    driver = relationship("User", back_populates="work_items")

    contributors = relationship(
        "User",
        secondary=work_item_contributors,
        back_populates="contributing_work_items",
        lazy="joined"
    )

    def soft_delete(self):
        self.is_deleted = True

    def restore(self):
        self.is_deleted = False

    def get_children(self):
        return []

    def get_parent_id(self):
        return None

    def has_parents(self):
        return False


class Task(WorkItem):
    __tablename__ = "tasks"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)

    complex_task_id = Column(Integer, ForeignKey("complex_tasks.id"))
    complex_task = relationship("ComplexTask", back_populates="tasks", foreign_keys=[complex_task_id])

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks", foreign_keys=[project_id])

    def has_parents(self):
        return None != self.project_id and None != self.complex_task_id

    def get_parent_id(self):
        parent_id = None
        if self.project_id:
            parent_id = self.project_id
        elif self.complex_task_id:
            parent_id = self.complex_task_id

        return parent_id


class ComplexTask(WorkItem):
    __tablename__ = "complex_tasks"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="complex_tasks", foreign_keys=[project_id])

    tasks = relationship(
        "Task",
        back_populates="complex_task",
        foreign_keys=[Task.complex_task_id],
        lazy="joined"
    )

    def has_parents(self):
        return None != self.project_id

    def get_parent_id(self):
        return self.project_id

    def get_children(self):
        return {"tasks": self.tasks}


class Project(WorkItem):
    __tablename__ = "projects"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)
    complex_tasks = relationship("ComplexTask", back_populates="project", foreign_keys=[ComplexTask.project_id], lazy="joined")
    tasks = relationship("Task", back_populates="project", foreign_keys=[Task.project_id], lazy="joined")

    def get_children(self):
        return {"complex_tasks": self.complex_tasks, "tasks": self.tasks}
