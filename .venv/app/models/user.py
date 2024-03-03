from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.user_role import UserRole
from app.db.database import Base
from app.models.team import Team
from app.models.user_team import user_team_association


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.VISITOR)
    signup_date = Column(DateTime, default=datetime.utcnow)

    work_items = relationship(
        "WorkItem",
        back_populates="owner",
        lazy="joined"
    )

    teams = relationship(
        "Team",
        secondary=user_team_association,
        back_populates="members",
        lazy='joined'
    )

    managed_teams = relationship("Team", back_populates="manager")


    def soft_delete(self):
        self.is_deleted = True

    def restore(self):
        self.is_deleted = False



