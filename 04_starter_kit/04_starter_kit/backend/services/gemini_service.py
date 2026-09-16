"""Wrapper du SDK Gemini avec persistance des appels en BDD.

Quatre méthodes principales :
- generer_texte : appel simple
- generer_structure : sortie JSON conforme à un schéma Pydantic
- generer_stream : streaming token par token
- analyser_fichier : multimodal (PDF, image, audio)
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.conversation import Conversation

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_client = genai.Client(api_key=settings.gemini_api_key)


def _persister(
    db: Session | None,
    user_input: str,
    ai_response: str,
    model: str,
    usage: types.GenerateContentResponseUsageMetadata | None,
    latency_ms: int,
) -> None:
    """Persiste l'appel en BDD si une session est fournie."""
    if db is None:
        return
    conv = Conversation(
        user_input=user_input[:2000],  # tronquer pour éviter d'exploser la BDD
        ai_response=ai_response[:5000],
        model=model,
        tokens_input=getattr(usage, "prompt_token_count", None) if usage else None,
        tokens_output=getattr(usage, "candidates_token_count", None) if usage else None,
        tokens_total=getattr(usage, "total_token_count", None) if usage else None,
        latency_ms=latency_ms,
    )
    db.add(conv)
    db.commit()


def generer_texte(
    prompt: str,
    *,
    db: Session | None = None,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_tokens: int | None = None,
    model: str | None = None,
) -> str:
    """Appel simple : prompt -> texte."""
    model = model or settings.default_model
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens or settings.max_tokens_default,
        system_instruction=system_instruction,
    )

    debut = time.perf_counter()
    response = _client.models.generate_content(model=model, contents=prompt, config=config)
    latency_ms = int((time.perf_counter() - debut) * 1000)

    _persister(db, prompt, response.text or "", model, response.usage_metadata, latency_ms)
    return response.text or ""


def generer_structure(
    prompt: str,
    schema: type[T],
    *,
    db: Session | None = None,
    system_instruction: str | None = None,
    model: str | None = None,
) -> T:
    """Force une sortie JSON conforme au schéma Pydantic donné."""
    model = model or settings.default_model
    config = types.GenerateContentConfig(
        temperature=0,
        response_mime_type="application/json",
        response_schema=schema,
        system_instruction=system_instruction,
        max_output_tokens=settings.max_tokens_default,
    )

    debut = time.perf_counter()
    response = _client.models.generate_content(model=model, contents=prompt, config=config)
    latency_ms = int((time.perf_counter() - debut) * 1000)

    _persister(db, prompt, response.text or "", model, response.usage_metadata, latency_ms)

    if response.parsed is None:
        raise ValueError("Sortie IA invalide : impossible de parser selon le schéma")
    return response.parsed  # type: ignore[return-value]


def generer_stream(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    model: str | None = None,
) -> Iterator[str]:
    """Streaming : yield les chunks de texte au fur et à mesure.

    Pas de persistance ici : à faire en aval si besoin (concaténer puis stocker).
    """
    model = model or settings.default_model
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
        max_output_tokens=settings.max_tokens_default,
    )
    stream = _client.models.generate_content_stream(model=model, contents=prompt, config=config)
    for chunk in stream:
        if chunk.text:
            yield chunk.text


def analyser_fichier(
    fichier_bytes: bytes,
    mime_type: str,
    prompt: str,
    *,
    db: Session | None = None,
    model: str | None = None,
) -> str:
    """Analyse multimodale d'un fichier (PDF, image, audio).

    Pour les fichiers > 20 Mo, utiliser plutôt l'API Files (à implémenter selon besoin projet).
    """
    if len(fichier_bytes) > 20 * 1024 * 1024:
        raise ValueError("Fichier trop gros (max 20 Mo en envoi direct)")

    model = model or settings.default_model
    contents = [
        types.Part.from_bytes(data=fichier_bytes, mime_type=mime_type),
        prompt,
    ]

    debut = time.perf_counter()
    response = _client.models.generate_content(model=model, contents=contents)
    latency_ms = int((time.perf_counter() - debut) * 1000)

    _persister(
        db, f"[fichier {mime_type}] {prompt}", response.text or "",
        model, response.usage_metadata, latency_ms,
    )
    return response.text or ""
