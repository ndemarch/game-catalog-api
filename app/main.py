#import asyncio
import os
from fastapi import FastAPI
from fastapi.routing import APIRouter
from contextlib import asynccontextmanager
from app.routes.character_routes import router as character_router
from app.routes.item_routes import router as item_router
from app.db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "development") != "test":
        await create_tables()
    yield

# creating the API instance with a lifespan
app = FastAPI(
    title="Game Catalog API",
    version="1.0.0",
    description="Manage characters and their loadouts",
    lifespan=lifespan
)

# registed routes
app.include_router(character_router)
app.include_router(item_router)
