import requests
from config import BACKEND_URL

def send_chat(query, session_id=None, preferred_agent=None):
    payload = {
        "query": query,
        "session_id": session_id
    }

    if preferred_agent and preferred_agent != "AUTO":
        payload["preferred_agent"] = preferred_agent

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()

def get_analytics():
    response = requests.get(
        f"{BACKEND_URL}/analytics/summary",
        timeout=10
    )
    return response.json() if response.status_code == 200 else {}

def health_check():
    try:
        return requests.get(f"{BACKEND_URL}/health", timeout=5).status_code == 200
    except:
        return False
