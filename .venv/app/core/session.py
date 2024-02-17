from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core import config

if config.settings.environment == "PYTEST":
    sqlalchemy_database_uri = config.settings.test_sqlalchemy_database_uri
else:
    sqlalchemy_database_uri = config.settings.database_url


async_engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
