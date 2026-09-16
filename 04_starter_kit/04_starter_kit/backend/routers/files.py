"""Endpoints multimodaux : analyse de fichier (PDF, image, audio)."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.common import AnalyseFichierResponse
from backend.services import gemini_service

router = APIRouter(prefix="/files", tags=["files"])

MIMES_AUTORISES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "audio/mpeg",
    "audio/wav",
}


@router.post("/analyser", response_model=AnalyseFichierResponse)
async def analyser_fichier(
    fichier: UploadFile = File(...),
    prompt: str = Form(default="Décris le contenu de ce fichier."),
    db: Session = Depends(get_db),
):
    """Analyse multimodale d'un fichier uploadé."""
    if fichier.content_type not in MIMES_AUTORISES:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté : {fichier.content_type}",
        )

    contenu = await fichier.read()
    if not contenu:
        raise HTTPException(status_code=400, detail="Fichier vide")

    try:
        analyse = gemini_service.analyser_fichier(
            contenu, fichier.content_type, prompt, db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA : {e}") from e

    return AnalyseFichierResponse(
        analyse=analyse,
        mime_type=fichier.content_type,
        taille_octets=len(contenu),
    )
