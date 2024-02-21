from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    work_items = relationship("WorkItem", back_populates="owner")


    def soft_delete(self):
        self.is_deleted = True

    def restore(self):
        self.is_deleted = False