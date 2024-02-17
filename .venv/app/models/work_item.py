from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    deadline = Column(DateTime, index=True)
    initial_date = Column(DateTime, index=True)
    finished_date = Column(DateTime, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="work_items")

class Task(WorkItem):
    __tablename__ = "tasks"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)

    feature_id = Column(Integer, ForeignKey("features.id"))
    feature = relationship("Feature", foreign_keys=[feature_id])

    epic_id = Column(Integer, ForeignKey('epics.id'))
    epic = relationship("Epic", back_populates="tasks", foreign_keys=[epic_id])


class Feature(WorkItem):
    __tablename__ = "features"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)

    epic_id = Column(Integer, ForeignKey('epics.id'))
    epic = relationship("Epic", back_populates="features", foreign_keys=[epic_id])

    tasks = relationship("Task", foreign_keys=[Task.feature_id])


class Epic(WorkItem):
    __tablename__ = "epics"

    id = Column(Integer, ForeignKey("work_items.id"), primary_key=True)
    features = relationship("Feature", foreign_keys=[Feature.epic_id])
    tasks = relationship("Task", foreign_keys=[Task.epic_id])
