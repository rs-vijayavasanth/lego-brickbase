"""Pydantic AI agent definitions for the LEGO BrickBase assistant.

This module defines specialist agents and a top-level router that delegates
to the right specialist based on user intent.
"""

from __future__ import annotations

from pydantic_ai import Agent

from app.config import LLM_MODEL
from app.tools import (
    get_color_usage,
    get_set_color_breakdown,
    get_set_details,
    get_set_minifigs,
    get_theme_hierarchy,
    get_theme_summary,
    get_yearly_trends,
    list_themes,
    search_parts,
    search_sets,
)

# ---------------------------------------------------------------------------
# 1. Set Recommender — suggests sets matching user criteria
# ---------------------------------------------------------------------------
set_recommender = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Set Recommender. Your job is to help users find the "
        "perfect LEGO set based on their preferences — theme, size, year, budget, "
        "color palette, or anything else they mention.\n\n"
        "Use the search_sets tool to query the catalogue, then rank and explain "
        "your recommendations. Always include set_number, name, year, theme, and "
        "part count. Be enthusiastic but concise."
    ),
    tools=[search_sets, get_set_details, get_set_color_breakdown],
)

# ---------------------------------------------------------------------------
# 2. Set Analyzer — deep-dive into a single set's composition
# ---------------------------------------------------------------------------
set_analyzer = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Set Analyzer. Given a set number or name, provide a "
        "thorough breakdown of the set: part count, unique parts, color palette, "
        "dominant color, transparency ratio, minifigures, and interesting facts.\n\n"
        "Use get_set_details, get_set_color_breakdown, and get_set_minifigs to "
        "gather data, then present it as a rich narrative. Include numbers but "
        "make it engaging."
    ),
    tools=[search_sets, get_set_details, get_set_color_breakdown, get_set_minifigs],
)

# ---------------------------------------------------------------------------
# 3. Theme Explorer — analytics across themes
# ---------------------------------------------------------------------------
theme_explorer = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Theme Explorer. Help users understand LEGO themes — "
        "their history, size, hierarchy, and statistics.\n\n"
        "Use get_theme_summary, list_themes, and get_theme_hierarchy to gather "
        "data. Present insights about how themes have evolved over time."
    ),
    tools=[list_themes, get_theme_summary, get_theme_hierarchy, get_yearly_trends],
)

# ---------------------------------------------------------------------------
# 4. Part & Color Specialist — lookup individual bricks and colors
# ---------------------------------------------------------------------------
part_color_specialist = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Part & Color Specialist. Answer questions about "
        "specific LEGO bricks, elements, or colors — how popular they are, "
        "which sets include them, and what categories they belong to.\n\n"
        "Use search_parts and get_color_usage to find data."
    ),
    tools=[search_parts, get_color_usage],
)

# ---------------------------------------------------------------------------
# 5. Trend Analyst — time-series and historical insights
# ---------------------------------------------------------------------------
trend_analyst = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Trend Analyst. Provide data-driven insights about how "
        "the LEGO catalogue has changed over time — average set sizes, color "
        "diversity trends, theme popularity, etc.\n\n"
        "Use get_yearly_trends and get_theme_summary. Present numbers and "
        "summarise patterns in a compelling way."
    ),
    tools=[get_yearly_trends, get_theme_summary, list_themes],
)

# ---------------------------------------------------------------------------
# 6. Set Comparator — compare multiple sets side-by-side
# ---------------------------------------------------------------------------
set_comparator = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO Set Comparator. When the user asks to compare two or "
        "more sets, fetch their details and present a structured side-by-side "
        "comparison covering: part count, unique parts, colors, themes, "
        "minifigures, and dominant color.\n\n"
        "Highlight the most interesting differences."
    ),
    tools=[search_sets, get_set_details, get_set_color_breakdown, get_set_minifigs],
)


# ---------------------------------------------------------------------------
# Router Agent — delegates to specialists
# ---------------------------------------------------------------------------
router_agent = Agent(
    LLM_MODEL,
    instructions=(
        "You are the LEGO BrickBase Assistant — a friendly, knowledgeable AI "
        "that helps people explore the world of LEGO.\n\n"
        "You have access to a rich analytics database covering 22,000+ sets, "
        "50,000+ parts, 200+ colors, and 500+ themes from Rebrickable.\n\n"
        "Based on what the user asks, use the appropriate tools to answer their "
        "question. You can:\n"
        "• Recommend sets based on criteria (theme, size, year, color)\n"
        "• Analyse a specific set in depth (composition, colors, minifigures)\n"
        "• Explore themes and their history\n"
        "• Look up specific parts or colors\n"
        "• Show trends over time\n"
        "• Compare sets side by side\n\n"
        "Be enthusiastic about LEGO! Use data to back up your answers. "
        "Format responses in Markdown with tables where appropriate."
    ),
    tools=[
        search_sets,
        get_set_details,
        get_set_color_breakdown,
        get_set_minifigs,
        get_theme_summary,
        list_themes,
        get_theme_hierarchy,
        search_parts,
        get_color_usage,
        get_yearly_trends,
    ],
)
