from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.db.db_session import engine
from app.db.base import Base
from app.configs.settings import settings


@asynccontextmanager
async def life_span(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("\n\nRDBMS table are created successfully!")
            
        yield
        
    finally:
        await engine.dispose()
        print("\n\nRDBMS engine disposed...")
        print("Application shutdown...")
        

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=life_span
)
