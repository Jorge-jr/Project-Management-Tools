import asyncio
from fastapi import FastAPI
from app.api.endpoints import user as user_router
from app.api.endpoints import auth as auth_router
from app.db.database import Base
from app.db.database import async_engine

# from app.api.models.user import UserOut

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Create FastAPI app
app = FastAPI()

# Include user_router
app.include_router(user_router.router, prefix='/user', tags=["user"])
app.include_router(auth_router.router, prefix='/auth', tags=["auth"])

# Run create_tables coroutine when the app starts
@app.on_event("startup")
async def startup_event():
    await create_tables()
