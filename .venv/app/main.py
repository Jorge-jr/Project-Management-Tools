import asyncio
from fastapi import FastAPI
from app.api.endpoints import user as user_router
from app.api.endpoints import auth as auth_router
from app.api.endpoints import work_item as work_item_router
from app.api.endpoints import team as team_router
from app.db.database import Base
from app.db.database import async_engine
from fastapi.middleware.cors import CORSMiddleware


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE", "PUT"],
    allow_headers=["*"]
)


app.include_router(user_router.router, prefix='/user', tags=["user"])
app.include_router(auth_router.router, prefix='/auth', tags=["auth"])
app.include_router(work_item_router.router, prefix='/work_item', tags=["work_item"])
app.include_router(team_router.router, prefix='/team', tags=["team"])

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.on_event("shutdown")
async def shutdown_event():
    # if env == 'testing': drop_tables()
    pass

# TODO: environment variables
# TODO: implement work_item.set_deadline and work_item.set_finished_date
# TODO: implement privileges (stakeholder, owner, admin, read-only)
# TODO: implement hard delete for work_items and users (admin only)
# TODO: create 'testing' environment (sqlite)
# TODO: implement logger
# TODO: Test invalid token scenarios


"""
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    hole = Column(Enum(SystemRole), default=SystemRole.VISITOR)

    # Define the relationship to WorkItem
    work_items = relationship("WorkItem", back_populates="owner")

class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owners = relationship("User", secondary="work_item_owner_association", back_populates="work_items")
    stakeholders = relationship("User", secondary="work_item_stakeholder_association")
    managers = relationship("User", secondary="work_item_manager_association")

# Define association tables for the many-to-many relationships
work_item_owner_association = Table(
    "work_item_owner_association",
    Base.metadata,
    Column("work_item_id", ForeignKey("work_items.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

work_item_stakeholder_association = Table(
    "work_item_stakeholder_association",
    Base.metadata,
    Column("work_item_id", ForeignKey("work_items.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

work_item_manager_association = Table(
    "work_item_manager_association",
    Base.metadata,
    Column("work_item_id", ForeignKey("work_items.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


"""
