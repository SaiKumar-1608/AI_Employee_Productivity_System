from llm import call_llm
from database import get_analytics_summary

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def handle(self, query: str, history=None):
        return call_llm(self.system_prompt, query, history)

class HRAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "HR Agent",
            "You are an internal HR assistant handling policies, leave, onboarding, and HR FAQs."
        )

class TechAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "Tech Support Agent",
            "You assist with internal tools, login issues, and technical troubleshooting."
        )

class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "Task Agent",
            "You help with sprint updates, deadlines, reminders, and task tracking."
        )

class AnalyticsAgent:
    def __init__(self):
        self.name = "Analytics Agent"

    def handle(self, query: str, history=None):
        data = get_analytics_summary()

        prompt = f"""
You are an enterprise productivity analyst.

Analytics data:
- Agent usage: {data['agent_usage']}
- Average latency (ms): {data['average_latency_ms']}
- Most used agent: {data['most_used_agent']}
- Peak usage hour: {data['peak_usage_hour']}

Respond with:
• Key observations (bullet points)
• What this indicates about employee behavior
• One actionable improvement suggestion
"""

        return call_llm(prompt, query)
