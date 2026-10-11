from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite local uniquement, aucun service externe (AD-11).
SQLITE_URL = "sqlite:///./talent_engine.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe de base declarative des entites SQLAlchemy.

    Aucune table n'est creee ici : le schema appartient aux stories qui
    introduisent les modeles (1.2+).
    """

# S'assurer que le moteur est accessible globalement (déjà défini ci-dessus)
