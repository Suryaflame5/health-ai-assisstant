"""
AI Desktop Assistant — Application Configuration

Loads environment variables and provides typed settings via Pydantic.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── LLM ──────────────────────────────────────────
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # ── Database ─────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./ai_assistant.db"
    database_url_sync: str = "sqlite:///./ai_assistant.db"

    # ── ChromaDB ─────────────────────────────────────
    chroma_persist_dir: str = "./chroma_data"
    chroma_host: str = "localhost"
    chroma_port: int = 8100

    # ── Voice ────────────────────────────────────────
    whisper_model: str = "base"
    tts_provider: str = "edge-tts"

    # ── Security ─────────────────────────────────────
    secret_key: str = "change-this-to-a-random-secret-key"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    # ── App ──────────────────────────────────────────
    log_level: str = "INFO"
    confirm_destructive_actions: bool = True
    max_automation_steps: int = 50
    screenshot_dir: str = "./screenshots"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def screenshot_path(self) -> Path:
        p = Path(self.screenshot_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p


def get_settings() -> Settings:
    """Factory function to create Settings instance."""
    return Settings()


settings = Settings()
