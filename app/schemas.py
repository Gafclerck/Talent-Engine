"""Modeles Pydantic (formes partagees, frontiere)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OffreBase(BaseModel):
    titre: str = Field(..., min_length=1)
    description: str | None = Field(default=None)


class OffreCreate(OffreBase):
    pass


class OffreUpdate(OffreBase):
    pass


class OffreRead(OffreBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titre: str
    description: str | None
    date_creation: datetime
    mapping: dict
    seuils_priorite: dict


# Formes JSON partagees (AD-5)
class Mapping(BaseModel):
    model_config = ConfigDict(extra="allow")

    # forme generique ; contenu precise arrive plus tard
    pass


class SeuilsPriorite(BaseModel):
    prioritaire_min: int | None = None
    a_examiner_min: int | None = None


class Palier(BaseModel):
    min: int
    max: int | None
    points: int


class ParametresPaliers(BaseModel):
    paliers: list[Palier]


class ParametresMotCle(BaseModel):
    mots_cles: list[list[str]]
    points_par_mot: int
    plafond: int


class ParametresPresence(BaseModel):
    longueur_min: int | None = None


class ParametresChoixListe(BaseModel):
    options: dict[str, int]


class ImportBatch(BaseModel):
    nom_fichier: str | None = None
    colonnes: list[str] = Field(default_factory=list)
    lignes: list[dict[str, str | None]] = Field(default_factory=list)
