"""Services CRUD pour les offres."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

from sqlalchemy.orm import Session

from app import models
from app import schemas


def creer_offre(session: Session, data: schemas.OffreCreate) -> models.Offre:
    offre = models.Offre(
        titre=data.titre,
        description=data.description,
        date_creation=datetime.utcnow(),
        mapping={},
        seuils_priorite={},
    )
    session.add(offre)
    session.flush()
    return offre


def lister_offres(session: Session) -> Sequence[models.Offre]:
    return session.query(models.Offre).order_by(models.Offre.id).all()


def obtenir_offre(session: Session, offre_id: int) -> models.Offre | None:
    return (
        session.query(models.Offre)
        .filter(models.Offre.id == offre_id)
        .first()
    )


def modifier_offre(
    session: Session, offre: models.Offre, data: schemas.OffreUpdate
) -> models.Offre:
    if data.titre is not None:
        offre.titre = data.titre
    offre.description = data.description
    session.flush()
    return offre
