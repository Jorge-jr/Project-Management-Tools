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
    type = Column(Enum(WorkItemType), default=WorkItemType.TASK)
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

    feature_id = Column(Integer, ForeignKey("features.id"))
    feature = relationship("Feature", back_populates="tasks", foreign_keys=[feature_id])

    epic_id = Column(Integer, ForeignKey('epics.id'))
    epic = relationship("Epic", back_populates="tasks", foreign_keys=[epic_id])

    def has_parents(self):
        return None != self.epic_id and None != self.feature_id

    def get_parent_id(self):
        parent_id = None
        if self.epic_id:
            parent_id = self.epic_id
        elif self.feature_id:
            parent_id = self.feature_id

        return parent_id


class Feature(WorkItem):
    __tablename__ = "features"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)

    epic_id = Column(Integer, ForeignKey('epics.id'))
    epic = relationship("Epic", back_populates="features", foreign_keys=[epic_id])

    tasks = relationship(
        "Task",
        back_populates="feature",
        foreign_keys=[Task.feature_id],
        lazy="joined"
    )

    def has_parents(self):
        return None != self.epic_id

    def get_parent_id(self):
        return self.epic_id

    def get_children(self):
        return {"tasks": self.tasks}


class Epic(WorkItem):
    __tablename__ = "epics"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)
    features = relationship("Feature", back_populates="epic", foreign_keys=[Feature.epic_id], lazy="joined")
    tasks = relationship("Task", back_populates="epic", foreign_keys=[Task.epic_id], lazy="joined")

    def get_children(self):
        return {"features": self.features, "tasks": self.tasks}
