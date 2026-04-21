# LEGO BrickBase — Agentic AI Layer

An **agentic AI interface** for the LEGO BrickBase analytics warehouse, built with **[Pydantic AI](https://pydantic.dev/docs/ai/overview/)**, **FastAPI**, and **Streamlit**.

Users interact with a natural-language chat interface that is backed by specialist AI agents. Each agent has access to a curated set of tools that query the Gold-layer star schema in Databricks, enabling data-grounded responses about 22,000+ LEGO sets, 50,000+ parts, 200+ colors, and 500+ themes.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Streamlit Chat UI  /  FastAPI REST + SSE                │
└────────────────────────┬─────────────────────────────────┘
                         │ user message
                         ▼
              ┌─────────────────────┐
              │    Router Agent     │  ← Pydantic AI Agent
              │  (intent detection) │
              └────────┬────────────┘
                       │ tool calls
         ┌─────────────┼───────────────────┐
         ▼             ▼                   ▼
   ┌───────────┐ ┌───────────┐     ┌─────────────┐
   │search_sets│ │get_theme_ │ ... │get_yearly_  │  ← Python tool functions
   │           │ │summary    │     │trends       │
   └─────┬─────┘ └─────┬─────┘     └──────┬──────┘
         │             │                   │
         ▼             ▼                   ▼
   ┌───────────────────────────────────────────────┐
   │        Databricks SQL Warehouse               │
   │   lego_brickbase.gold.*  (Star Schema)        │
   │   dim_set · dim_part · dim_color · dim_theme  │
   │   fct_set_inventory · fct_set_composition · … │
   └───────────────────────────────────────────────┘
```

## Agents

| Agent | Purpose | Tools |
|---|---|---|
| **Router** | General-purpose assistant; uses all tools | All |
| **Set Recommender** | Find sets by theme, year, size, color | `search_sets`, `get_set_details`, `get_set_color_breakdown` |
| **Set Analyzer** | Deep-dive into a single set's composition | `get_set_details`, `get_set_color_breakdown`, `get_set_minifigs` |
| **Theme Explorer** | Explore theme history and stats | `list_themes`, `get_theme_summary`, `get_theme_hierarchy` |
| **Part & Color Specialist** | Lookup parts and color statistics | `search_parts`, `get_color_usage` |
| **Trend Analyst** | Historical trends over time | `get_yearly_trends`, `get_theme_summary` |
| **Set Comparator** | Side-by-side set comparison | `get_set_details`, `get_set_color_breakdown`, `get_set_minifigs` |

## Data Tools

Every tool is a pure Python function that builds a `SELECT` query against the Gold star schema and returns rows as `list[dict]`.

| Tool | Description |
|---|---|
| `search_sets` | Filter sets by name, theme, year range, part count |
| `get_set_details` | Full composition metrics for a set |
| `get_set_color_breakdown` | Color distribution within a set |
| `get_set_minifigs` | Minifigures included in a set |
| `get_theme_summary` | Aggregated stats for a theme |
| `list_themes` | Top themes by set count |
| `get_theme_hierarchy` | Parent → child theme relationships |
| `search_parts` | Find parts by name or category |
| `get_color_usage` | Color popularity across the catalogue |
| `get_yearly_trends` | Year-over-year set/part/color trends |

## Features for Portfolio

This project demonstrates:

1. **Agentic AI with Pydantic AI** — type-safe agents, structured output, tool calling, streaming
2. **Multi-agent architecture** — specialist agents with a router pattern
3. **Data-grounded AI** — every response backed by real warehouse queries (no hallucinated numbers)
4. **Medallion lakehouse** — Bronze/Silver/Gold on Databricks with Delta Lake
5. **REST API** — FastAPI with sync + streaming SSE endpoints
6. **Interactive UI** — Streamlit chat interface with agent selector
7. **Production patterns** — environment-based config, SQL injection protection, connection management

## Quick Start

### 1. Install dependencies

```bash
cd agent
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Databricks + OpenAI credentials
```

### 3. Run the API server

```bash
uvicorn app.api:app --reload --port 8000
```

### 4. Run the Streamlit UI

```bash
streamlit run app/ui.py
```

### 5. Try the API directly

```bash
# List agents
curl http://localhost:8000/agents

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Recommend large Star Wars sets", "agent": "recommender"}'

# Stream
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "How has LEGO Technic evolved?"}'
```

## Project Structure

```
agent/
├── pyproject.toml          # Package definition & dependencies
├── .env.example            # Environment variable template
├── app/
│   ├── __init__.py
│   ├── config.py           # Environment config loader
│   ├── db.py               # Databricks SQL connector wrapper
│   ├── models.py           # Pydantic output models
│   ├── tools.py            # Agent tools (SQL query functions)
│   ├── agents.py           # Pydantic AI agent definitions
│   ├── api.py              # FastAPI endpoints
│   └── ui.py               # Streamlit chat interface
└── tests/
    └── test_tools.py       # Unit tests for tool functions
```

## Tech Stack

| Component | Technology |
|---|---|
| Agent framework | [Pydantic AI](https://pydantic.dev/docs/ai/overview/) |
| Data models | [Pydantic v2](https://docs.pydantic.dev/) |
| API layer | [FastAPI](https://fastapi.tiangolo.com/) |
| Chat UI | [Streamlit](https://streamlit.io/) |
| Data warehouse | [Databricks](https://www.databricks.com/) (Delta Lake, Unity Catalog) |
| LLM provider | OpenAI (configurable) |

## Extending

- **Add a new tool**: create a function in `tools.py` and register it in the appropriate agent's `tools=[]` list in `agents.py`.
- **Add a new agent**: define an `Agent(...)` in `agents.py` with instructions + tools, then add it to the `AGENTS` dict in both `api.py` and `ui.py`.
- **Switch LLM provider**: change `LLM_MODEL` in `.env` — Pydantic AI supports OpenAI, Anthropic, Gemini, and many more.
- **Add structured output**: use the Pydantic models in `models.py` as `output_type=` on any agent.
- **Add observability**: add `logfire.configure(); logfire.instrument_pydantic_ai()` for full OpenTelemetry tracing.
