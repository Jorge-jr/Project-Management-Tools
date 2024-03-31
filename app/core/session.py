from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base


if settings.environment == "TESTING":
    print(f"Connecting to test database: {settings.database_url}")
    sqlalchemy_database_uri = settings.database_url
else:
    print(f'Connecting to dev database: {settings.database_url}')
    sqlalchemy_database_uri = settings.database_url

async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
