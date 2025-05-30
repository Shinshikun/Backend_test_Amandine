from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from api import sessionmanager
from api.routers.user import router as user_router
from api.routers.auth import router as auth_router
from src.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()



app = FastAPI(lifespan=lifespan, title="Test Amandine", docs_url="/api/docs")

app.include_router(user_router)
app.include_router(auth_router)


