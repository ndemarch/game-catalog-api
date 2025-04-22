import os
from dotenv import load_dotenv
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


# create async engine for test db
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
