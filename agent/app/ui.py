"""Streamlit chat UI for the LEGO BrickBase Agent."""

from __future__ import annotations

import asyncio

import streamlit as st

# Must be the first Streamlit call
st.set_page_config(
    page_title="LEGO BrickBase Assistant",
    page_icon="🧱",
    layout="wide",
)

# Lazy-import agents so Streamlit hot-reload stays fast
from app.agents import (  # noqa: E402
    router_agent,
    set_analyzer,
    set_comparator,
    set_recommender,
    theme_explorer,
    trend_analyst,
    part_color_specialist,
)

AGENTS = {
    "🤖 Auto (Router)": router_agent,
    "🎯 Set Recommender": set_recommender,
    "🔍 Set Analyzer": set_analyzer,
    "🏰 Theme Explorer": theme_explorer,
    "🧩 Part & Color Specialist": part_color_specialist,
    "📈 Trend Analyst": trend_analyst,
    "⚖️ Set Comparator": set_comparator,
}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🧱 LEGO BrickBase")
    st.caption("Agentic AI Analytics over 22,000+ LEGO sets")

    agent_choice = st.selectbox("Choose an agent", list(AGENTS.keys()))

    st.divider()
    st.markdown(
        "**Example questions:**\n"
        "- Recommend Star Wars sets with 1000+ pieces\n"
        "- Analyse set 75192-1 (Millennium Falcon)\n"
        "- How has the Technic theme evolved?\n"
        "- What is the most popular LEGO color?\n"
        "- Compare 10294-1 and 10312-1\n"
        "- Show set-size trends from 2000–2025"
    )

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# User input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask me anything about LEGO..."):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream the agent answer
    agent = AGENTS[agent_choice]
    with st.chat_message("assistant"):
        placeholder = st.empty()
        result = [""]

        async def _stream():
            async with agent.run_stream(prompt) as stream:
                async for chunk in stream.stream_text(delta=True):
                    result[0] += chunk
                    placeholder.markdown(result[0] + "▌")
            placeholder.markdown(result[0])

        asyncio.run(_stream())

    st.session_state.messages.append({"role": "assistant", "content": result[0]})
