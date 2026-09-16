"""Setup SQLAlchemy : engine, session, Base, dépendance FastAPI."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.config import settings

# Pour SQLite il faut désactiver le check_same_thread
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """Dépendance FastAPI : ouvre une session BDD par requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
