"""FastAPI application — exposes the LEGO BrickBase agent as an HTTP API."""

from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.agents import (
    router_agent,
    set_analyzer,
    set_comparator,
    set_recommender,
    theme_explorer,
    trend_analyst,
    part_color_specialist,
)

app = FastAPI(
    title="LEGO BrickBase Agent API",
    version="0.1.0",
    description="Agentic AI layer over the LEGO BrickBase analytics warehouse",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENTS = {
    "router": router_agent,
    "recommender": set_recommender,
    "analyzer": set_analyzer,
    "themes": theme_explorer,
    "parts": part_color_specialist,
    "trends": trend_analyst,
    "compare": set_comparator,
}


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    agent: str = Field(
        default="router",
        description="Which specialist agent to use. Defaults to the router.",
    )


class ChatResponse(BaseModel):
    reply: str
    agent_used: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/agents")
async def list_agents() -> dict[str, list[str]]:
    """Return available agent names."""
    return {"agents": list(AGENTS.keys())}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Send a message to the LEGO assistant and get a response."""
    agent = AGENTS.get(req.agent, router_agent)
    result = await agent.run(req.message)
    return ChatResponse(reply=result.output, agent_used=req.agent)


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """Stream the agent response token-by-token via SSE."""
    agent = AGENTS.get(req.agent, router_agent)

    async def _generate():
        async with agent.run_stream(req.message) as stream:
            async for chunk in stream.stream_text(delta=True):
                yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(_generate(), media_type="text/event-stream")
