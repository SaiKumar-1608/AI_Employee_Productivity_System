# 🚀 AI Employee Productivity & Support System

An intelligent AI-powered system designed to help employees quickly get answers about HR policies, technical issues, task management, and productivity insights — all through a multi-agent conversational interface.

---

## 🌟 Features

### 🤖 Multi-Agent AI Architecture
- Specialized agents for **HR, Tech Support, Task Management, and Productivity Analytics**
- Auto-routing of queries using **LLM-based intent detection**  
- Optional manual agent override for transparency and control

### 🧠 Persistent Memory and Analytics
- Conversation memory stored in **SQLite**
- Analytics metrics including:
  - Agent usage counts
  - Average response latency
  - Peak usage hours
- Analytics Agent provides **interpreted insights**, not just raw stats

### 💬 Frontend (Streamlit UI)
- Clean chat interface with:
  - Session metrics
  - Agent identity badges
  - Latency indicators
  - Demo mode with sample prompts
- Analytics dashboard:
  - Bar charts for usage and latency
  - Exportable JSON report

---
## 📁 Project Structure
```
SprintFour/
├── backend/ # FastAPI backend
│ ├── main.py
│ ├── agents.py
│ ├── router.py
│ ├── llm.py
│ ├── database.py
│ ├── memory.py
│ ├── interactions.db # SQLite database
│ ├── requirements.txt
│ └── .env
├── frontend/ # Streamlit frontend
│ ├── app.py
│ ├── api_client.py
│ ├── config.py
│ └── requirements.txt
└── README.md
```

---

## 🛠️ Backend — FastAPI

The backend handles:
- LLM calls for intent detection and response generation
- Session-based memory
- Interaction logging
- Analytics aggregation

📍 Endpoints:
- `POST /chat` — Responds to user queries (auto/manual agent)
- `GET /analytics/summary` — Returns analytics metrics
- `GET /health` — Health check

---

## 🔧 Frontend — Streamlit Chat & Dashboard

The frontend allows:
- Chat interface with agent responses
- Manual agent selection
- Demo prompt support
- Analytics visualization

To run:

```bash
cd frontend
streamlit run app.py

## 📁 Project Structure

