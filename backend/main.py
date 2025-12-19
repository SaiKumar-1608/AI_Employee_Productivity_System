from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import time

from router import route_query
from database import init_db, log_interaction, get_analytics_summary
from memory import get_memory, update_memory
from agents import HRAgent, TechAgent, TaskAgent, AnalyticsAgent

app = FastAPI(title="AI Employee Productivity & Support System")

# 🔥 Agent registry for manual override
AGENT_MAP = {
    "HR": HRAgent(),
    "TECH": TechAgent(),
    "TASK": TaskAgent(),
    "ANALYTICS": AnalyticsAgent()
}

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None
    preferred_agent: str | None = None   # 🔥 NEW

class ChatResponse(BaseModel):
    session_id: str
    agent: str
    response: str
    latency_ms: float

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    history = get_memory(session_id)

    start = time.time()

    # 🔥 Hybrid routing logic
    if request.preferred_agent and request.preferred_agent in AGENT_MAP:
        agent = AGENT_MAP[request.preferred_agent]
    else:
        agent = route_query(request.query)

    answer = agent.handle(request.query, history)

    latency_ms = round((time.time() - start) * 1000, 2)

    update_memory(session_id, "user", request.query)
    update_memory(session_id, "assistant", answer)

    log_interaction(
        session_id,
        request.query,
        agent.name,
        answer,
        latency_ms
    )

    return ChatResponse(
        session_id=session_id,
        agent=agent.name,
        response=answer,
        latency_ms=latency_ms
    )

@app.get("/analytics/summary")
def analytics_summary():
    return get_analytics_summary()
