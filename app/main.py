from fastapi import FastAPI

from app.routers import user
from app.database import connect, disconnect

app = FastAPI()

@app.on_event("startup")
async def start_db():
    connect()

@app.on_event("shutdown")
async def close_db():
    disconnect()

app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)
