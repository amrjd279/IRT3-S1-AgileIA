"""Fixtures pytest partagées."""

import os

# Force une fausse clé pour les tests (sinon Settings refuse de s'instancier)
os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest
from fastapi.testclient import TestClient

from backend.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def reset_db():
    """Recréer les tables avant chaque test pour l'isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Client HTTP de test."""
    return TestClient(app)
