"""Configuration centralisée chargée depuis .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application.

    Toutes les valeurs sont chargées depuis .env (jamais hardcodées).
    """

    # API IA
    gemini_api_key: str
    default_model: str = "gemini-3.6-flash"

    # App
    app_name: str = "Mon Projet IA"
    environment: str = "development"

    # CORS : liste d'origines séparées par virgules dans .env
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"

    # Limites
    max_tokens_default: int = 1000
    rate_limit_per_minute: int = 20

    # Base de données
    database_url: str = "sqlite:///./app.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
