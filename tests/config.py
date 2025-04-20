import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# loading the test environment variables
load_dotenv(".env.test")
# testing database credentials
MYSQL_USER = os.getenv("TEST_MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("TEST_MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("TEST_MYSQL_DATABASE", "test_game_catalog")
MYSQL_HOST = os.getenv("TEST_MYSQL_HOST", "test-db")

TEST_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
# create async engine for test db
async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
