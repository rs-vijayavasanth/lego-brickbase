"""Agent tools — functions the LLM can call to retrieve LEGO data.

Every tool function is a plain function (no RunContext needed) that queries
the Gold layer in Databricks and returns JSON-serialisable data.
"""

from __future__ import annotations

from app.config import DATABRICKS_CATALOG, DATABRICKS_SCHEMA_GOLD
from app.db import run_query

_GOLD = f"{DATABRICKS_CATALOG}.{DATABRICKS_SCHEMA_GOLD}"


# ---- SET tools ------------------------------------------------------------

def search_sets(
    name_contains: str | None = None,
    theme_name: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    min_parts: int | None = None,
    max_parts: int | None = None,
    limit: int = 20,
) -> list[dict]:
    """Search LEGO sets by name, theme, year range, or part count.

    Args:
        name_contains: Substring to match in the set name (case-insensitive).
        theme_name: Exact or partial theme name to filter on.
        year_from: Minimum release year (inclusive).
        year_to: Maximum release year (inclusive).
        min_parts: Minimum total-part count.
        max_parts: Maximum total-part count.
        limit: Maximum rows to return (default 20, max 100).
    """
    clauses: list[str] = []
    if name_contains:
        clauses.append(f"LOWER(s.set_name) LIKE LOWER('%{_esc(name_contains)}%')")
    if theme_name:
        clauses.append(f"LOWER(s.theme_name) LIKE LOWER('%{_esc(theme_name)}%')")
    if year_from is not None:
        clauses.append(f"s.year >= {int(year_from)}")
    if year_to is not None:
        clauses.append(f"s.year <= {int(year_to)}")
    if min_parts is not None:
        clauses.append(f"c.total_parts >= {int(min_parts)}")
    if max_parts is not None:
        clauses.append(f"c.total_parts <= {int(max_parts)}")

    where = " AND ".join(clauses) if clauses else "1=1"
    safe_limit = min(int(limit), 100)

    sql = f"""
        SELECT s.set_number, s.set_name, s.year, s.theme_name,
               c.total_parts, c.total_unique_parts, c.total_unique_colors,
               c.dominant_color_name, c.number_of_minifigs
        FROM {_GOLD}.dim_set s
        JOIN {_GOLD}.fct_set_composition c ON s.set_key = c.set_key
        WHERE {where}
        ORDER BY c.total_parts DESC
        LIMIT {safe_limit}
    """
    return run_query(sql)


def get_set_details(set_number: str) -> list[dict]:
    """Get full composition details for a specific LEGO set by set_number.

    Args:
        set_number: The Rebrickable set number, e.g. '75192-1'.
    """
    sql = f"""
        SELECT s.set_number, s.set_name, s.year, s.theme_name,
               c.total_parts, c.total_unique_parts, c.total_unique_colors,
               c.dominant_color_name, c.dominant_part_category,
               c.pct_transparent_parts, c.pct_spare_parts, c.number_of_minifigs
        FROM {_GOLD}.dim_set s
        JOIN {_GOLD}.fct_set_composition c ON s.set_key = c.set_key
        WHERE s.set_number = '{_esc(set_number)}'
    """
    return run_query(sql)


def get_set_color_breakdown(set_number: str) -> list[dict]:
    """Get the color distribution for a specific LEGO set.

    Args:
        set_number: The Rebrickable set number.
    """
    sql = f"""
        SELECT dc.color_name, dc.rgb, dc.is_transparent,
               SUM(fi.quantity) AS quantity
        FROM {_GOLD}.fct_set_inventory fi
        JOIN {_GOLD}.dim_set s ON fi.set_key = s.set_key
        JOIN {_GOLD}.dim_color dc ON fi.color_key = dc.color_key
        WHERE s.set_number = '{_esc(set_number)}'
        GROUP BY dc.color_name, dc.rgb, dc.is_transparent
        ORDER BY quantity DESC
    """
    return run_query(sql)


def get_set_minifigs(set_number: str) -> list[dict]:
    """Get the minifigures included in a specific LEGO set.

    Args:
        set_number: The Rebrickable set number.
    """
    sql = f"""
        SELECT m.minifig_name, m.minifig_number, fm.quantity, m.number_of_parts
        FROM {_GOLD}.fct_set_minifigs fm
        JOIN {_GOLD}.dim_set s ON fm.set_key = s.set_key
        JOIN {_GOLD}.dim_set m ON fm.minifig_key = m.set_key
        WHERE s.set_number = '{_esc(set_number)}'
    """
    return run_query(sql)


# ---- THEME tools ----------------------------------------------------------

def get_theme_summary(theme_name: str) -> list[dict]:
    """Get aggregated statistics for a LEGO theme.

    Args:
        theme_name: Full or partial theme name (case-insensitive).
    """
    sql = f"""
        SELECT *
        FROM {_GOLD}.fct_theme_summary
        WHERE LOWER(theme_name) LIKE LOWER('%{_esc(theme_name)}%')
        ORDER BY total_sets DESC
        LIMIT 10
    """
    return run_query(sql)


def list_themes(limit: int = 30) -> list[dict]:
    """List the top themes by total number of sets.

    Args:
        limit: Maximum number of themes to return.
    """
    safe_limit = min(int(limit), 100)
    sql = f"""
        SELECT theme_name, root_theme_name, total_sets,
               avg_parts_per_set, year_first_set, year_latest_set
        FROM {_GOLD}.fct_theme_summary
        ORDER BY total_sets DESC
        LIMIT {safe_limit}
    """
    return run_query(sql)


def get_theme_hierarchy(theme_name: str) -> list[dict]:
    """Get the parent-child hierarchy for a theme.

    Args:
        theme_name: Full or partial theme name.
    """
    sql = f"""
        SELECT theme_name, parent_theme_name, root_theme_name, hierarchy_depth
        FROM {_GOLD}.dim_theme_hierarchy
        WHERE LOWER(theme_name) LIKE LOWER('%{_esc(theme_name)}%')
           OR LOWER(root_theme_name) LIKE LOWER('%{_esc(theme_name)}%')
        ORDER BY hierarchy_depth
    """
    return run_query(sql)


# ---- PART / COLOR tools ---------------------------------------------------

def search_parts(
    name_contains: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Search for LEGO parts by name or category.

    Args:
        name_contains: Substring match on part name.
        category: Exact or partial part category name.
        limit: Max rows.
    """
    clauses: list[str] = []
    if name_contains:
        clauses.append(f"LOWER(p.part_name) LIKE LOWER('%{_esc(name_contains)}%')")
    if category:
        clauses.append(f"LOWER(p.part_category_name) LIKE LOWER('%{_esc(category)}%')")
    where = " AND ".join(clauses) if clauses else "1=1"
    safe_limit = min(int(limit), 100)

    sql = f"""
        SELECT p.part_number, p.part_name, p.part_category_name,
               u.total_sets_used_in, u.total_quantity_across_sets,
               u.most_common_color, u.first_year_appeared, u.latest_year_appeared
        FROM {_GOLD}.dim_part p
        JOIN {_GOLD}.fct_part_usage u ON p.part_key = u.part_key
        WHERE {where}
        ORDER BY u.total_sets_used_in DESC
        LIMIT {safe_limit}
    """
    return run_query(sql)


def get_color_usage(color_name: str | None = None, limit: int = 20) -> list[dict]:
    """Get color usage statistics across the LEGO catalogue.

    Args:
        color_name: Optional color name filter (partial match).
        limit: Max rows.
    """
    where = (
        f"LOWER(color_name) LIKE LOWER('%{_esc(color_name)}%')"
        if color_name
        else "1=1"
    )
    safe_limit = min(int(limit), 100)

    sql = f"""
        SELECT color_name, rgb, is_transparent, color_family,
               total_sets_featuring_color, total_parts_in_color,
               total_quantity, top_theme
        FROM {_GOLD}.fct_color_usage
        WHERE {where}
        ORDER BY total_quantity DESC
        LIMIT {safe_limit}
    """
    return run_query(sql)


# ---- TREND tools ----------------------------------------------------------

def get_yearly_trends(
    theme_name: str | None = None,
    year_from: int = 1950,
    year_to: int = 2026,
) -> list[dict]:
    """Get yearly trends for sets, parts, and colors.

    Args:
        theme_name: Optional theme filter (partial match).
        year_from: Start year.
        year_to: End year.
    """
    theme_filter = (
        f"AND LOWER(s.theme_name) LIKE LOWER('%{_esc(theme_name)}%')"
        if theme_name
        else ""
    )
    sql = f"""
        SELECT s.year,
               COUNT(DISTINCT s.set_number) AS total_sets,
               AVG(c.total_parts) AS avg_parts,
               AVG(c.total_unique_colors) AS avg_unique_colors
        FROM {_GOLD}.dim_set s
        JOIN {_GOLD}.fct_set_composition c ON s.set_key = c.set_key
        WHERE s.year BETWEEN {int(year_from)} AND {int(year_to)}
              {theme_filter}
        GROUP BY s.year
        ORDER BY s.year
    """
    return run_query(sql)


# ---- helpers --------------------------------------------------------------

def _esc(value: str) -> str:
    """Minimal SQL-injection prevention for string literals interpolated into queries.

    Strips single-quotes, semicolons, and comment markers.
    """
    return (
        str(value)
        .replace("'", "")
        .replace(";", "")
        .replace("--", "")
        .replace("/*", "")
        .replace("*/", "")
    )
