import logging

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Talent Engine")


@app.get("/sante")
def sante() -> dict[str, str]:
    return {"statut": "ok"}
