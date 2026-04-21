"""Unit tests for tool functions (mocked DB layer)."""

from __future__ import annotations

from unittest.mock import patch

import pytest


MOCK_ROWS = [
    {
        "set_number": "75192-1",
        "set_name": "Millennium Falcon",
        "year": 2017,
        "theme_name": "Star Wars",
        "total_parts": 7541,
        "total_unique_parts": 1639,
        "total_unique_colors": 27,
        "dominant_color_name": "Light Bluish Gray",
        "number_of_minifigs": 8,
    }
]


@patch("app.tools.run_query", return_value=MOCK_ROWS)
def test_search_sets_returns_results(mock_query):
    from app.tools import search_sets

    results = search_sets(theme_name="Star Wars", min_parts=5000)
    assert len(results) == 1
    assert results[0]["set_number"] == "75192-1"
    mock_query.assert_called_once()


@patch("app.tools.run_query", return_value=MOCK_ROWS)
def test_get_set_details(mock_query):
    from app.tools import get_set_details

    results = get_set_details("75192-1")
    assert len(results) == 1
    mock_query.assert_called_once()


@patch("app.tools.run_query", return_value=[])
def test_search_sets_empty(mock_query):
    from app.tools import search_sets

    results = search_sets(name_contains="nonexistent_set_xyz")
    assert results == []


def test_esc_strips_dangerous_chars():
    from app.tools import _esc

    assert "'" not in _esc("O'Brien")
    assert ";" not in _esc("DROP;TABLE")
    assert "--" not in _esc("--comment")
