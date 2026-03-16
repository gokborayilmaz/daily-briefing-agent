from datetime import datetime

from upsonic import Agent, Task

from config.constants import BRIEFING_MODEL, DB_PATH, USER_NAME
from models.briefing import MorningBriefing
from tools.email_tool import fetch_unread_emails
from tools.calendar_tool import fetch_todays_calendar


class ExecutiveBriefingAgent:
    """Delivers a concise morning briefing from emails and calendar,
    remembering follow-ups across sessions."""

    def __init__(self, model: str = BRIEFING_MODEL):
        self.agent = Agent(
            model=model,
            name="Executive Briefing Assistant",
            role="Personal executive assistant",
            goal=(
                "Deliver a clear, prioritized morning briefing that helps "
                "the executive start their day prepared and in control"
            ),
            instructions=f"""You are the executive assistant for {USER_NAME}.
Your responsibilities:
1. Fetch unread emails and today's calendar using the provided tools.
2. Classify emails by urgency — only truly time-sensitive items are urgent.
3. Cross-reference emails with calendar events to surface connections
   (e.g. an email from an attendee of an upcoming meeting).
4. Identify follow-ups the executive should track.
5. Produce a concise, actionable briefing — no fluff.

Style guidelines:
- Be professional but warm.
- Lead with what matters most.
- Always mention specific times, names, and deadlines.
- Keep the summary to 3-4 sentences maximum.

Today's date: {datetime.now().strftime('%A, %B %d, %Y')}""",

            # --- Memory: persist across sessions ---
            memory=self._create_memory(),

            # --- Reflection: let agent self-check urgency classification ---
            reflection=True,

            # --- Safety: anonymize PII if data leaves the system ---
            agent_policy=self._create_agent_policy(),
        )

    @staticmethod
    def _create_memory():
        """Create SQLite-backed memory with full session history."""
        from upsonic.storage import SQLiteStorage
        from upsonic.storage.memory.memory import Memory

        storage = SQLiteStorage(DB_PATH)
        return Memory(
            storage=storage,
            session_id="executive_briefing",
            full_session_memory=True,
        )

    @staticmethod
    def _create_agent_policy():
        """Create agent policy with PII anonymization."""
        try:
            from upsonic.safety_engine import Policy

            return Policy(
                rules=["Anonymize any PII (personal emails, phone numbers, "
                       "addresses) before including them in the briefing output."],
            )
        except ImportError:
            return None

    def generate_briefing(self) -> MorningBriefing:
        """Generate a structured morning briefing.

        Uses tools to fetch emails and calendar, then produces
        a Pydantic-validated MorningBriefing object.
        """
        task = Task(
            description=(
                f"Generate today's morning briefing for {USER_NAME}. "
                "First fetch unread emails using the fetch_unread_emails tool, "
                "then fetch today's calendar using the fetch_todays_calendar tool. "
                "Analyze everything and produce a complete briefing."
            ),
            tools=[fetch_unread_emails, fetch_todays_calendar],
            response_format=MorningBriefing,
        )

        self.agent.do(task)
        return task.response

    def chat(self, message: str) -> str:
        """Send a follow-up message and get a response.

        Memory is shared, so the agent remembers the briefing
        and any previous follow-up conversations.
        """
        task = Task(description=message)
        self.agent.do(task)
        return task.response
