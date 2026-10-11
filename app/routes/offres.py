"""Routes HTML pour la gestion des offres."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session

from app import database, schemas
from app.services import offre_service

router = APIRouter()

env = Environment(loader=FileSystemLoader("app/templates"), autoescape=True)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def _await_form_data(request: Request) -> dict:
    form = await request.form()
    return dict(form)


@router.get("/offres", response_class=HTMLResponse)
def liste_offres(request: Request, db: Session = Depends(get_db)):
    offres = offre_service.lister_offres(db)
    template = env.get_template("offres/liste.html")
    return HTMLResponse(
        template.render(request=request, offres=offres), status_code=200
    )


@router.get("/offres/creer", response_class=HTMLResponse)
def formulaire_creation(request: Request):
    template = env.get_template("offres/formulaire.html")
    return HTMLResponse(
        template.render(request=request, offre=None), status_code=200
    )


@router.post("/offres/creer")
async def creer_offre(request: Request, db: Session = Depends(get_db)):
    form_data = await _await_form_data(request)
    titre = str(form_data.get("titre", "")).strip()
    description = form_data.get("description")
    data = schemas.OffreCreate(
        titre=titre, description=description or None
    )
    offre_service.creer_offre(db, data)
    db.commit()
    return RedirectResponse(url="/offres", status_code=303)


@router.get("/offres/{offre_id}", response_class=HTMLResponse)
def detail_offre(offre_id: int, request: Request, db: Session = Depends(get_db)):
    offre = offre_service.obtenir_offre(db, offre_id)
    if not offre:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    template = env.get_template("offres/detail.html")
    return HTMLResponse(
        template.render(request=request, offre=offre), status_code=200
    )


@router.get("/offres/{offre_id}/modifier", response_class=HTMLResponse)
def formulaire_edition(
    offre_id: int, request: Request, db: Session = Depends(get_db)
):
    offre = offre_service.obtenir_offre(db, offre_id)
    if not offre:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    template = env.get_template("offres/formulaire.html")
    return HTMLResponse(
        template.render(request=request, offre=offre), status_code=200
    )


@router.post("/offres/{offre_id}/modifier")
async def modifier_offre(
    offre_id: int, request: Request, db: Session = Depends(get_db)
):
    offre = offre_service.obtenir_offre(db, offre_id)
    if not offre:
        raise HTTPException(status_code=404, detail="Offre introuvable")
    form_data = await _await_form_data(request)
    titre = str(form_data.get("titre", "")).strip()
    description = form_data.get("description")
    data = schemas.OffreUpdate(titre=titre, description=description or None)
    offre_service.modifier_offre(db, offre, data)
    db.commit()
    return RedirectResponse(url="/offres", status_code=303)
