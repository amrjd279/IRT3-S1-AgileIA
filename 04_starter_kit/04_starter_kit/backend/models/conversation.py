"""Exemple de modèle SQLAlchemy : historique des conversations IA."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.database import Base


class Conversation(Base):
    """Historique d'une interaction avec l'IA, persistée pour audit et stats."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    model = Column(String(50), nullable=False)
    tokens_input = Column(Integer)
    tokens_output = Column(Integer)
    tokens_total = Column(Integer)
    latency_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Conversation id={self.id} tokens={self.tokens_total}>"
