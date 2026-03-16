import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Executive Briefing Agent",
    page_icon="☀️",
    layout="wide",
)


# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Required to run the agent.",
    )
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.divider()
    st.caption("Powered by **Upsonic** · gpt-4o")


# ── Header ───────────────────────────────────────────────────────
st.title("☀️ Executive Briefing Agent")
st.markdown(
    "Your AI executive assistant — fetches emails & calendar, "
    "delivers a prioritized morning briefing, and remembers follow-ups."
)

if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()


# ── Agent ────────────────────────────────────────────────────────
@st.cache_resource
def get_agent():
    from agents.briefing_agent import ExecutiveBriefingAgent
    return ExecutiveBriefingAgent()


# ── Generate Briefing ────────────────────────────────────────────
if st.button("🌅 Generate Morning Briefing", type="primary", use_container_width=True):
    agent = get_agent()
    with st.spinner("Fetching emails and calendar, analyzing priorities..."):
        briefing = agent.generate_briefing()
        st.session_state["briefing"] = briefing

# Display stored briefing
briefing = st.session_state.get("briefing")
if briefing:
    st.divider()

    # Greeting
    st.header(briefing.greeting)
    st.caption(f"📅 {briefing.date}")

    # Layout: 2 columns
    col_left, col_right = st.columns(2)

    with col_left:
        # Urgent emails
        if briefing.urgent_emails:
            st.subheader(f"🔴 Urgent Emails ({len(briefing.urgent_emails)})")
            for email in briefing.urgent_emails:
                with st.container(border=True):
                    st.markdown(f"**{email.subject}**")
                    st.caption(f"From: {email.sender} · {email.received_at}")
                    st.write(email.snippet)

        # Other emails
        if briefing.other_emails:
            st.subheader(f"📬 Other Emails ({len(briefing.other_emails)})")
            for email in briefing.other_emails:
                with st.expander(f"{email.sender} — {email.subject}"):
                    st.write(email.snippet)
                    st.caption(f"Received: {email.received_at}")

    with col_right:
        # Schedule
        if briefing.today_schedule:
            st.subheader(f"📅 Today's Schedule ({len(briefing.today_schedule)})")
            for event in briefing.today_schedule:
                with st.container(border=True):
                    st.markdown(f"**{event.title}**")
                    st.caption(
                        f"⏰ {event.start_time} – {event.end_time}"
                        + (f" · 📍 {event.location}" if event.location else "")
                    )
                    if event.attendees:
                        st.write(f"👥 {', '.join(event.attendees)}")

        # Follow-ups
        if briefing.follow_ups:
            st.subheader(f"📌 Follow-Ups ({len(briefing.follow_ups)})")
            for item in briefing.follow_ups:
                icon = "🔴" if item.priority == "high" else "🟡"
                with st.container(border=True):
                    st.markdown(f"{icon} **{item.contact}** — {item.topic}")
                    st.caption(f"Due: {item.due_date}")

    # Summary
    st.divider()
    st.subheader("💡 Summary")
    st.info(briefing.summary)

# ── Chat Follow-up ──────────────────────────────────────────────
st.divider()
st.subheader("💬 Follow-up Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a follow-up question..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    agent = get_agent()
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.chat(prompt)
        st.write(response)

    st.session_state["messages"].append(
        {"role": "assistant", "content": response}
    )
