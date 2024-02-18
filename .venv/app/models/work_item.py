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
    is_deleted = Column(Boolean, default=False)

    owner = relationship("User", back_populates="work_items")

    def soft_delete(self):
        self.is_deleted = True

    def restore(self):
        self.is_deleted = False

    @classmethod
    def get_all(cls, session, include_deleted=False):
        if include_deleted:
            return session.query(cls).all()
        else:
            return session.query(cls).filter(cls.is_deleted == False).all()

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
