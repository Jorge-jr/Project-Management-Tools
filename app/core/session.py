from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


if settings.environment == "TESTING":
    sqlalchemy_database_uri = settings.test_database_url
else:
    sqlalchemy_database_uri = settings.database_url

async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


Base = declarative_base()