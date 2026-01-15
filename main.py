from fastapi import FastAPI
from app.routes import item, auth, user, permission, role
from app.db.session import engine
from app.models.base import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(item.router, prefix="/api/items", tags=["Items"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(role.router, prefix="/api/roles", tags=["Roles"])
app.include_router(permission.router, prefix="/api/permissions", tags=["Permissions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}