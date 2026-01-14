from fastapi import FastAPI
from app.routes import item
from app.db.session import engine
from app.models.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.include_router(item.router, prefix="/api/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}