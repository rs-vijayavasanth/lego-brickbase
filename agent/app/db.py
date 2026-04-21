"""Databricks SQL connectivity — thin wrapper around databricks-sql-connector."""

from __future__ import annotations

from typing import Any

from databricks import sql as databricks_sql

from app.config import DATABRICKS_HOST, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN


def get_connection() -> databricks_sql.client.Connection:
    """Return a fresh Databricks SQL Warehouse connection."""
    return databricks_sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )


def run_query(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Execute *query* and return rows as a list of dicts.

    The caller is responsible for ensuring the query is safe.
    Only SELECT statements are permitted.
    """
    normalized = query.strip().rstrip(";")
    if not normalized.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(normalized, parameters=params)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()
