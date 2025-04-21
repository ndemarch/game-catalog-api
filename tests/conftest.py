import pytest
import asyncio
import pytest_asyncio
from app.db import Base
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.config import async_engine, TestingSessionLocal

# ---------- FIXTURES ---------- #

@pytest.fixture(scope="session")
def event_loop():
    # create a new event loop for the test session
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    # create and destroy the test database schema
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(autouse=True)
async def override_get_db(monkeypatch, db_session):
    # override the get_db dependency with the test session
    async def _override():
        yield db_session
    monkeypatch.setattr("app.db.get_db", _override)

@pytest_asyncio.fixture
async def client():
    # provides an AsyncClient for making test requests
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
