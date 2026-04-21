"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _require(var: str) -> str:
    val = os.getenv(var)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {var}")
    return val


# --- LLM -----------------------------------------------------------------
ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "anthropic:claude-haiku-4-5-20251001")

# --- Databricks -----------------------------------------------------------
DATABRICKS_HOST: str = _require("DATABRICKS_HOST")
DATABRICKS_HTTP_PATH: str = _require("DATABRICKS_HTTP_PATH")
DATABRICKS_TOKEN: str = _require("DATABRICKS_TOKEN")
DATABRICKS_CATALOG: str = os.getenv("DATABRICKS_CATALOG", "lego_brickbase")
DATABRICKS_SCHEMA_GOLD: str = os.getenv("DATABRICKS_SCHEMA_GOLD", "gold")
