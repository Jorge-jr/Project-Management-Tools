from app.core import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


if config.settings.environment == "TESTING":
    sqlalchemy_database_uri = config.settings.test_database_url
else:
    sqlalchemy_database_uri = config.settings.database_url

async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
