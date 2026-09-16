"""Script d'initialisation de la base de données.

Usage : python -m backend.scripts.init_db
"""

from backend.database import Base, engine
from backend.models import Conversation  # noqa: F401 (import nécessaire pour create_all)


def init_db() -> None:
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print(f"Tables créées : {list(Base.metadata.tables.keys())}")


if __name__ == "__main__":
    init_db()
