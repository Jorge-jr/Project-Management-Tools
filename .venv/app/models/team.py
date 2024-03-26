from app.core.session import Base
from app.models.user_team import user_team_association
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    members = relationship("User", secondary=user_team_association, back_populates="teams")
    manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User", back_populates="managed_teams")
