from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine, Base
from routers import users, subscriptions, currencies
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    pass

app = FastAPI(title="Currency Tracker API", lifespan=lifespan)

app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(currencies.router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API отслеживания валют. Перейдите на /docs для Swagger UI"}
