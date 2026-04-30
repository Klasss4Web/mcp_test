import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MCP_SERVER_URL: str = os.getenv("MCP_SERVER_URL", "https://order-mcp-74afyau24q-uc.a.run.app/mcp")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

@lru_cache()
def get_settings() -> Settings:
    return Settings()
