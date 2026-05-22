from upsonic import Agent, Task
from upsonic.storage.memory import Memory
from upsonic.storage.sqlite import SqliteStorage
from upsonic.reflection import ReflectionConfig
from config.constants import BRIEFING_MODEL, USER_NAME, DB_PATH
from models.briefing import MorningBriefing
from tools.email_tool import fetch_unread_emails
from tools.calendar_tool import fetch_todays_calendar


# --- MCP DEFINITION (FOR REAL GOOGLE CONNECTION) ---
# To use  Gmail/Calendar data with MCP, uncomment the class below.
# class GoogleWorkspaceMCP:
#     """Google Workspace (Gmail & Calendar) MCP Server"""
#     command = "uvx"
#     args = ["mcp-server-google-workspace"]
# ----------------------------------------------


class ExecutiveBriefingAgent:
    def __init__(self, model: str = BRIEFING_MODEL):
        
        # 1. Creating Storage and Memory
        self.storage = SqliteStorage(db_file=DB_PATH)
        self.memory = Memory(
            storage=self.storage,
            session_id="executive_briefing_session",
            user_id=USER_NAME,
            full_session_memory=True,
            summary_memory=True,
            user_analysis_memory=True,
            model=model
        )

        # 2. Reflection Settings
        ref_config = None
        if ReflectionConfig:
            ref_config = ReflectionConfig(max_iterations=2, acceptance_threshold=0.8)

        # 3. Agent Creating
        self.agent = Agent(
            name="Executive Briefing Assistant",
            role="Personal executive assistant",
            model=model,
            goal="Deliver a prioritized morning briefing and answer follow-up questions.",
            instructions=f"You are the executive assistant for {USER_NAME}. Always use tools to check the calendar when asked about schedules.",
            memory=self.memory, 
            reflection=True if ref_config else False,
            reflection_config=ref_config,
            debug=True 
        )

    def generate_briefing(self) -> MorningBriefing:
        briefing_task = Task(
            f"Generate today's morning briefing for {USER_NAME}.",
            # Use this tools line for MCP connection
          #  tools= [GoogleWorkspaceMCP]
            # Use this tools line for Quick try
            tools=[fetch_unread_emails, fetch_todays_calendar], 
            response_format=MorningBriefing
        )
        self.agent.do(briefing_task)
        return briefing_task.response

    def chat(self, message: str) -> str:
        chat_task = Task(
            message,
        )
        self.agent.do(chat_task)
        return chat_task.response