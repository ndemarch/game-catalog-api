from fastapi import FastAPI
from app.routes.character_routes import router as character_router
from app.routes.loadout_routes import router as loadout_router
from app.db import Base, engine

# initialize database tables
Base.metadata.create_all(bind=engine)
# create API instance
app = FastAPI(
    title="Game Catalog API",
    version="1.0.0",
    description="Manage characters and their loadouts"
)
# register routes
app.include_router(character_router, prefix="/characters", tags=["Characters"])
app.include_router(loadout_router, prefix="/loadouts", tags=["Loadouts"])
