import asyncio
from fastapi import FastAPI
from app.api.endpoints import user as user_router
from app.api.endpoints import auth as auth_router
from app.api.endpoints import work_item as work_item_router
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

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.on_event("shutdown")
async def shutdown_event():
    # if env == 'testing': drop_tables()
    pass

# TODO: environment variables
# TODO: implement soft delete for work_items and users
# TODO: implement privileges (stakeholder, owner, admin, read-only)
# TODO: implement hard delete for work_items and users (admin only)
# TODO: create 'testing' environment (sqlite)
# TODO: implement logger
# TODO: implement users/me/work_items endpoint
# TODO: implement users/{id}/work_items endpoint
