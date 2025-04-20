import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# loading the test environment variables
load_dotenv(".env.test")
# testing database credentials
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test_game_catalog")
MYSQL_HOST = os.getenv("MYSQL_HOST", "test-db")

TEST_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
# create async engine for test db
async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
