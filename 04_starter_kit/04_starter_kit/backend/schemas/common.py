"""Schémas Pydantic communs au projet."""

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Requête simple : une question."""

    question: str = Field(min_length=1, max_length=2000)


class QuestionResponse(BaseModel):
    """Réponse simple."""

    reponse: str
    tokens_utilises: int | None = None
    conversation_id: int | None = None


class AnalyseFichierResponse(BaseModel):
    """Résultat d'une analyse multimodale."""

    analyse: str
    mime_type: str
    taille_octets: int
