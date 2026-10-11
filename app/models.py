"""Entites SQLAlchemy."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database import Base


class Offre(Base):
    """Offre d'emploi."""

    __tablename__ = "offres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, default=datetime.utcnow
    )
    mapping: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    seuils_priorite: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict
    )

    grilles: Mapped[list[Grille]] = relationship(
        "Grille", back_populates="offre", cascade="all, delete-orphan"
    )
    imports: Mapped[list[Import]] = relationship(
        "Import", back_populates="offre", cascade="all, delete-orphan"
    )
    candidats: Mapped[list[Candidat]] = relationship(
        "Candidat", back_populates="offre", cascade="all, delete-orphan"
    )


class Grille(Base):
    """Grille de scoring d'une offre."""

    __tablename__ = "grilles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    offre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("offres.id"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    date_modification: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, default=datetime.utcnow
    )

    offre: Mapped[Offre] = relationship("Offre", back_populates="grilles")
    criteres: Mapped[list[Critere]] = relationship(
        "Critere", back_populates="grille", cascade="all, delete-orphan"
    )


class Critere(Base):
    """Critère d'une grille."""

    __tablename__ = "criteres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grille_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("grilles.id"), nullable=False, index=True
    )
    libelle: Mapped[str] = mapped_column(String(255), nullable=False)
    champ: Mapped[str] = mapped_column(String(100), nullable=False)
    type_regle: Mapped[str] = mapped_column(String(50), nullable=False)
    parametres: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    poids_max: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    eliminatoire: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    ordre: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    grille: Mapped[Grille] = relationship("Grille", back_populates="criteres")


class Import(Base):
    """Import de candidats."""

    __tablename__ = "imports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    offre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("offres.id"), nullable=False, index=True
    )
    nom_fichier: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_import: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, default=datetime.utcnow
    )
    total_lignes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nb_importes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nb_ignores: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nb_rejetes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rapport_erreurs: Mapped[dict | list] = mapped_column(
        JSON, nullable=False, default=list
    )

    offre: Mapped[Offre] = relationship("Offre", back_populates="imports")
    candidats: Mapped[list[Candidat]] = relationship(
        "Candidat", back_populates="import_", cascade="all, delete-orphan"
    )


class Candidat(Base):
    """Candidat importé."""

    __tablename__ = "candidats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    offre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("offres.id"), nullable=False, index=True
    )
    import_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("imports.id"), nullable=False, index=True
    )
    nom: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_normalise: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    reponses: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    donnees_brutes: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict
    )
    statut: Mapped[str | None] = mapped_column(String(50), nullable=True)
    drapeaux: Mapped[list | dict] = mapped_column(
        JSON, nullable=False, default=list
    )
    date_candidature: Mapped[datetime | None] = mapped_column(
        Date, nullable=True
    )

    offre: Mapped[Offre] = relationship("Offre", back_populates="candidats")
    import_: Mapped[Import] = relationship(
        "Import", back_populates="candidats", foreign_keys=[import_id]
    )
    score: Mapped[Score | None] = relationship(
        "Score", back_populates="candidat", uselist=False
    )


class Score(Base):
    """Score d'un candidat."""

    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("candidats.id"), nullable=False, unique=True
    )
    version_grille: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    priorite: Mapped[str | None] = mapped_column(String(50), nullable=True)
    detail: Mapped[list | dict] = mapped_column(
        JSON, nullable=False, default=list
    )
    date_calcul: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, default=datetime.utcnow
    )

    candidat: Mapped[Candidat] = relationship("Candidat", back_populates="score")
