"""Pydantic models used as structured output types across agents."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Set Recommender
# ---------------------------------------------------------------------------
class SetRecommendation(BaseModel):
    """A single LEGO set recommendation."""

    set_number: str = Field(description="Rebrickable set number, e.g. '75192-1'")
    set_name: str
    year: int
    theme_name: str
    total_parts: int
    reason: str = Field(description="Why this set matches the user's criteria")


class SetRecommendationList(BaseModel):
    """Agent output: a ranked list of recommended LEGO sets."""

    recommendations: list[SetRecommendation]
    summary: str = Field(description="Natural-language summary of the recommendations")


# ---------------------------------------------------------------------------
# Set Analyzer
# ---------------------------------------------------------------------------
class ColorBreakdown(BaseModel):
    color_name: str
    rgb: str
    quantity: int
    percentage: float


class SetAnalysis(BaseModel):
    """Deep-dive analysis of a single LEGO set."""

    set_number: str
    set_name: str
    year: int
    theme_name: str
    total_parts: int
    unique_parts: int
    unique_colors: int
    dominant_color: str
    dominant_part_category: str
    pct_transparent: float
    minifig_count: int
    color_breakdown: list[ColorBreakdown]
    narrative: str = Field(description="A human-readable story about this set")


# ---------------------------------------------------------------------------
# Theme Explorer
# ---------------------------------------------------------------------------
class ThemeInsight(BaseModel):
    """Analytics summary for a LEGO theme."""

    theme_name: str
    root_theme: str
    total_sets: int
    avg_parts_per_set: float
    year_first_set: int
    year_latest_set: int
    active_span_years: int
    total_minifigs: int
    unique_parts_used: int
    unique_colors_used: int
    narrative: str


# ---------------------------------------------------------------------------
# Part / Color lookup
# ---------------------------------------------------------------------------
class PartInfo(BaseModel):
    part_number: str
    part_name: str
    category: str
    total_sets_used_in: int
    total_quantity: int
    most_common_color: str
    first_year: int
    latest_year: int
    is_active: bool


class ColorInfo(BaseModel):
    color_name: str
    rgb: str
    is_transparent: bool
    color_family: str
    total_sets: int
    total_parts: int
    total_quantity: int


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------
class SetComparison(BaseModel):
    """Side-by-side comparison of two or more sets."""

    sets: list[SetAnalysis]
    comparison_narrative: str = Field(
        description="Narrative highlighting the similarities and differences"
    )


# ---------------------------------------------------------------------------
# Trend Analysis
# ---------------------------------------------------------------------------
class YearTrend(BaseModel):
    year: int
    total_sets: int
    avg_parts: float
    avg_unique_colors: float


class TrendAnalysis(BaseModel):
    """Trend analysis over time for a theme or the entire catalogue."""

    scope: str = Field(description="Theme name or 'All Themes'")
    trends: list[YearTrend]
    narrative: str
