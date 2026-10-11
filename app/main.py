import logging

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import offres
from app.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title=settings.app_title)

# Créer les tables au démarrage
Base.metadata.create_all(bind=engine)

# Inclure les routers
app.include_router(offres.router)


@app.get("/sante")
def sante() -> dict[str, str]:
    return {"statut": "ok"}
