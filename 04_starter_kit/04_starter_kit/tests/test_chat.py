"""Tests des endpoints chat avec mock du service Gemini."""

from unittest.mock import patch


def test_root(client):
    """Le root retourne un statut OK."""
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health(client):
    """Le healthcheck répond."""
    r = client.get("/health")
    assert r.status_code == 200


def test_chat_simple_ok(client):
    """L'endpoint chat simple retourne une réponse mockée."""
    with patch("backend.routers.chat.gemini_service.generer_texte", return_value="Bonjour !"):
        r = client.post("/chat/simple", json={"question": "Salut"})
    assert r.status_code == 200
    data = r.json()
    assert data["reponse"] == "Bonjour !"


def test_chat_simple_validation_question_vide(client):
    """Une question vide est rejetée par Pydantic."""
    r = client.post("/chat/simple", json={"question": ""})
    assert r.status_code == 422


def test_chat_simple_validation_question_trop_longue(client):
    """Une question trop longue est rejetée."""
    r = client.post("/chat/simple", json={"question": "x" * 3000})
    assert r.status_code == 422


def test_chat_simple_gere_erreur_ia(client):
    """En cas d'erreur du service IA, on renvoie une 500 propre."""
    with patch(
        "backend.routers.chat.gemini_service.generer_texte",
        side_effect=Exception("Quota dépassé"),
    ):
        r = client.post("/chat/simple", json={"question": "Salut"})
    assert r.status_code == 500
    assert "Quota dépassé" in r.json()["detail"]
