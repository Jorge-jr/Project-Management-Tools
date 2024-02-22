from sqlalchemy import Table, ForeignKey, Column, Integer, Enum
from app.models.user_role import UserRole
from app.db.database import Base

user_team_association = Table(
    "user_team_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
    Column("role", Enum(UserRole)),
)