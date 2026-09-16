"""Endpoints conversationnels : chat simple, structuré, streaming."""

from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.common import QuestionRequest, QuestionResponse
from backend.services import gemini_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/simple", response_model=QuestionResponse)
async def chat_simple(req: QuestionRequest, db: Session = Depends(get_db)):
    """Appel basique : question -> réponse texte."""
    try:
        reponse = gemini_service.generer_texte(req.question, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA : {e}") from e
    return QuestionResponse(reponse=reponse)


@router.post("/stream")
async def chat_stream(req: QuestionRequest):
    """Streaming : envoie les chunks au fur et à mesure."""

    def generer():
        try:
            for chunk in gemini_service.generer_stream(req.question):
                yield chunk
        except Exception as e:
            yield f"\n[ERREUR : {e}]"

    return StreamingResponse(generer(), media_type="text/plain")


# Exemple d'extraction structurée
class Polarite(str, Enum):
    """Enum plutot que str : Gemini ne peut choisir qu'une valeur connue."""

    positif = "positif"
    negatif = "negatif"
    neutre = "neutre"


class Sentiment(BaseModel):
    polarite: str
    score_confiance: float = Field(ge=0, le=1)
    justification: str
    langue_detectee: str | None = Field(
        default=None,
        description="Langue du texte analyse, en francais",
    )


@router.post("/sentiment", response_model=Sentiment)
async def analyser_sentiment(req: QuestionRequest, db: Session = Depends(get_db)):
    """Démo de sortie structurée Pydantic : analyse de sentiment d'un texte."""
    try:
        return gemini_service.generer_structure(
            f"Analyse le sentiment du texte suivant : {req.question}",
            schema=Sentiment,
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA : {e}") from e
