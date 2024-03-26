from pydantic import BaseModel


class Team(BaseModel):
    id: int
    name: str
    manager_id: int


class TeamCreateRequest(Team):
    manager_id: int
