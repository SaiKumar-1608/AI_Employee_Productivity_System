from agents import HRAgent, TechAgent, TaskAgent, AnalyticsAgent
from llm import call_llm

hr_agent = HRAgent()
tech_agent = TechAgent()
task_agent = TaskAgent()
analytics_agent = AnalyticsAgent()

ALLOWED = {"HR", "TECH", "TASK", "ANALYTICS"}

INTENT_PROMPT = """
Classify the user query into exactly ONE category:
HR, TECH, TASK, ANALYTICS.
Return ONLY the category name.
"""

def detect_intent(query: str):
    intent = call_llm(INTENT_PROMPT, query)
    return intent.strip().upper()

def route_query(query: str):
    try:
        intent = detect_intent(query)
        if intent not in ALLOWED:
            return tech_agent
    except:
        return tech_agent

    if intent == "HR":
        return hr_agent
    elif intent == "TASK":
        return task_agent
    elif intent == "ANALYTICS":
        return analytics_agent
    else:
        return tech_agent
