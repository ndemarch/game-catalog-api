from fastapi import FastAPI
from app.routes.character_routes import router as character_router
from app.routes.item_routes import router as item_router
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
app.include_router(character_router)
app.include_router(item_router)

# add root endpoint
#@app.get("/")
#async def root():
#    return {"message": "Welcome to the Game Catalog API!"}
## add health check endpoint
#@app.get("/health")
#async def health_check():
#    return {"status": "healthy"}
## add documentation endpoint
#@app.get("/docs")
#async def docs():
#    return {"message": "API documentation can be found at /docs"}