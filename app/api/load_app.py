from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importation ajoutée

from app.api import sessionmanager
from app.api.routers.user import router as user_router
from app.api.routers.auth import router as auth_router
from app.api.routers.task import router as task_router
from app.api.routers.label import router as label_router
from app.src.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()



app = FastAPI(lifespan=lifespan, title="Test Amandine", docs_url="/api/docs")

# Configuration CORS
origins = [
    "http://localhost",          # Ajoutez l'origine de votre frontend Vue.js
    "http://localhost:8080",     # Si vous utilisez le port par défaut de `vue-cli-service serve`
    "http://localhost:5173",     # Si vous utilisez le port par défaut de Vite (`npm run dev`)
    "http://127.0.0.1:5173",   # Parfois nécessaire aussi
    # Ajoutez d'autres origines si nécessaire (par exemple, votre frontend déployé)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Les origines autorisées à faire des requêtes
    allow_credentials=True, # Autorise les cookies/authentification par en-tête
    allow_methods=["*"],    # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],    # Autorise tous les en-têtes
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(label_router)
