from app.api.endpoints import auth as auth_router
from app.api.endpoints import project as project_router
from app.api.endpoints import complex_task as complex_task_router
from app.api.endpoints import task as task_router
from app.api.endpoints import team as team_router
from app.api.endpoints import user as user_router
from app.api.endpoints import work_item as work_item_router
from app.db.database import Base
from app.db.database import async_engine
from fastapi import FastAPI
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
app.include_router(project_router.router, prefix='/project', tags=["project"])
app.include_router(complex_task_router.router, prefix='/complex_task', tags=["complex_task"])
app.include_router(task_router.router, prefix='/task', tags=["task"])


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    # if env == 'testing': drop_tables()
    pass


# TODO: environment variables
# TODO: implement privileges (stakeholder, driver, admin, read-only)
# TODO: implement hard delete for work_items and users (admin only)
# TODO: create 'testing' environment (sqlite)
# TODO: implement logger
# TODO: Test invalid token scenarios
# TODO: Create dependencies for each class when needed (add_parent, add_contributor, etc)
# TODO: Clean code Refactor