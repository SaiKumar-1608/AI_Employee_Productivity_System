import streamlit as st
import json
from api_client import send_chat, get_analytics, health_check

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Employee Support",
    layout="wide"
)

# -------------------------------------------------
# UI Styling (CSS)
# -------------------------------------------------
st.markdown("""
<style>
.app-title {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.app-subtitle {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 1.5rem;
}
.chat-card {
    background: #ffffff;
    padding: 14px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.hr { border-left: 5px solid #1976d2; }
.tech { border-left: 5px solid #2e7d32; }
.task { border-left: 5px solid #ef6c00; }
.analytics { border-left: 5px solid #6a1b9a; }
.info-card {
    background: #f4f8ff;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.metric-card {
    background: #ffffff;
    padding: 14px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Helper mappings
# -------------------------------------------------
AGENT_META = {
    "HR Agent": {"emoji": "🧑‍💼", "class": "hr"},
    "Tech Support Agent": {"emoji": "🛠", "class": "tech"},
    "Task Agent": {"emoji": "📅", "class": "task"},
    "Analytics Agent": {"emoji": "📊", "class": "analytics"},
}

AGENT_MODE_MAP = {
    "Auto (Recommended)": None,
    "🧑‍💼 HR Agent": "HR",
    "🛠 Tech Agent": "TECH",
    "📅 Task Agent": "TASK",
    "📊 Analytics Agent": "ANALYTICS",
}

DEMO_PROMPTS = [
    "What is the leave policy for new employees?",
    "I am unable to log in to the internal dashboard.",
    "What is my sprint deadline this week?",
    "Give me productivity insights from employee interactions."
]

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.markdown("**AI Employee Productivity & Support System**")

backend_ok = health_check()
st.sidebar.success("Backend Connected ✅" if backend_ok else "Backend Down ❌")

selected_mode = st.sidebar.selectbox(
    "Agent Mode",
    list(AGENT_MODE_MAP.keys())
)
preferred_agent = AGENT_MODE_MAP[selected_mode]

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🆕 New Conversation"):
    st.session_state.messages = []
    st.session_state.session_id = None
    st.sidebar.success("Conversation reset")

show_history = st.sidebar.checkbox("Show Chat History", True)
demo_mode = st.sidebar.checkbox("Demo Mode")

page = st.sidebar.radio(
    "Navigate",
    ["Chat Assistant", "Analytics Dashboard"]
)

# -------------------------------------------------
# Chat Assistant Page
# -------------------------------------------------
if page == "Chat Assistant":

    st.markdown("<div class='app-title'>💬 AI Employee Assistant</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-subtitle'>Smart, multi-agent support for HR, Tech, Tasks, and Productivity</div>",
        unsafe_allow_html=True
    )

    # KPI cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>🧠 Session Active</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<div class='metric-card'>🤖 Mode<br><b>{selected_mode}</b></div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div class='metric-card'>💬 Messages<br><b>{len(st.session_state.messages)}</b></div>",
            unsafe_allow_html=True
        )

    # Empty state
    if not st.session_state.messages:
        st.markdown("""
        <div class="info-card">
        👋 <b>Welcome!</b><br><br>
        Ask about <b>HR policies</b>, <b>technical issues</b>, <b>tasks</b>,
        or <b>productivity insights</b>.<br><br>
        <b>Auto mode</b> intelligently routes queries.<br>
        You may manually override the agent from the sidebar.
        </div>
        """, unsafe_allow_html=True)

    if show_history:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if demo_mode:
        user_input = st.selectbox("Choose a demo prompt", [""] + DEMO_PROMPTS)
    else:
        user_input = st.chat_input("Ask something...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = send_chat(
                    user_input,
                    st.session_state.session_id,
                    preferred_agent
                )

                if not result or "agent" not in result:
                    st.error("Backend error. Please try again.")
                    st.stop()

                st.session_state.session_id = result["session_id"]

                agent_name = result["agent"]
                meta = AGENT_META.get(agent_name, {"emoji": "🤖", "class": ""})

                st.markdown(
                    f"""
                    <div class="chat-card {meta['class']}">
                        <b>{meta['emoji']} {agent_name}</b><br><br>
                        {result["response"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(f"⏱ Latency: {result['latency_ms']} ms")

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                f"**{meta['emoji']} {agent_name}**\n\n"
                f"{result['response']}\n\n"
                f"_Latency: {result['latency_ms']} ms_"
            )
        })

# -------------------------------------------------
# Analytics Dashboard Page
# -------------------------------------------------
if page == "Analytics Dashboard":
    st.markdown("<div class='app-title'>📊 Productivity Analytics</div>", unsafe_allow_html=True)

    data = get_analytics()
    if not data:
        st.warning("No analytics data available yet.")
        st.stop()

    st.success(
        f"🔍 **Key Insight:** Most queries are handled by "
        f"**{data['most_used_agent']}**, indicating higher demand."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Most Used Agent", data["most_used_agent"])
    col2.metric(
        "Peak Usage Hour",
        f"{data['peak_usage_hour']}:00" if data["peak_usage_hour"] else "N/A"
    )
    col3.metric("Total Agents", len(data["agent_usage"]))

    st.subheader("Agent Usage")
    st.bar_chart(data["agent_usage"])

    st.subheader("Average Latency (ms)")
    st.bar_chart(data["average_latency_ms"])

    st.download_button(
        "⬇️ Download Analytics (JSON)",
        json.dumps(data, indent=2),
        "analytics_report.json",
        "application/json"
    )

    st.info("Insights are generated from real interaction logs stored in SQLite.")
