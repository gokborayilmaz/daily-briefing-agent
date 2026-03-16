# ☀️ Executive Briefing Agent

An AI-powered executive assistant that pulls your daily schedule and unread emails to deliver a concise, prioritized morning briefing — and remembers follow-ups across sessions.

## Architecture

This agent uses:
- **1 Specialized Agent** — Executive Briefing Assistant (Tier 1: single Agent + Task)
- **Persistent Memory** — SQLite with `full_session_memory=True` for cross-session context
- **Reflection** — Self-checks urgency classification before delivering the briefing
- **Safety Engine** — AgentPolicy with PII anonymization rules
- **Structured Output** — Pydantic `MorningBriefing` model as `response_format`
- **Custom Tools** — Simulated email/calendar fetchers (easily swappable for real APIs or MCP)

### Agent Details

| Property | Value |
|---|---|
| **Name** | Executive Briefing Assistant |
| **Role** | Personal executive assistant |
| **Model** | `openai/gpt-4o` |
| **Memory** | SQLite (`full_session_memory=True`) |
| **Reflection** | Enabled (urgency re-evaluation) |
| **Safety** | AgentPolicy (PII anonymization) |

## Installation

```bash
git clone https://github.com/Upsonic/Agent-1-Executive-Briefing-Agent.git
cd Agent-1-Executive-Briefing-Agent

# Create virtual environment
uv venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### CLI Mode

```bash
python main.py
```

Generates a formatted morning briefing and opens an interactive chat for follow-up questions.

### Streamlit UI

```bash
streamlit run streamlit_app.py
```

Two-column layout with urgent emails, schedule, follow-ups, and a chat interface.

## File Structure

```
Agent-1-Executive-Briefing-Agent/
├── README.md               # This file
├── main.py                 # CLI entry point
├── streamlit_app.py        # Streamlit UI entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
├── LICENSE
├── agents/
│   ├── __init__.py
│   └── briefing_agent.py   # Core agent (Memory + Reflection + Safety)
├── tools/
│   ├── __init__.py
│   ├── email_tool.py       # Simulated email fetcher
│   └── calendar_tool.py    # Simulated calendar fetcher
├── models/
│   ├── __init__.py
│   └── briefing.py         # Pydantic models (MorningBriefing, Email, etc.)
└── config/
    └── constants.py        # Model name, DB path, user preferences
```

## Configuration

Edit `config/constants.py` to customize:

| Constant | Default | Description |
|---|---|---|
| `BRIEFING_MODEL` | `openai/gpt-4o` | LLM model to use |
| `DB_PATH` | `executive_briefing_memory.db` | SQLite memory file path |
| `USER_NAME` | `Alex` | Executive's name (used in prompts) |
| `USER_TIMEZONE` | `US/Eastern` | Timezone for scheduling |

## Connecting Real Email & Calendar via MCP

The simulated tools in `tools/` can be replaced with real MCP (Model Context Protocol) integrations in two simple steps:

### Step 1 — Install an MCP Server

For **Gmail + Google Calendar**, use the [Google Workspace MCP Server](https://github.com/nichochar/google-workspace-mcp):

```bash
# Install the MCP server
pip install google-workspace-mcp

# Or any other MCP server that exposes email/calendar tools
```

### Step 2 — Connect to the Agent

Replace the function tools with an MCP handler in `agents/briefing_agent.py`:

```python
from upsonic import Agent, Task
from upsonic.tools.mcp import MCPHandler

class ExecutiveBriefingAgent:
    def __init__(self, model="openai/gpt-4o"):
        # Connect to MCP server (email + calendar tools auto-discovered)
        self.mcp_handler = MCPHandler("http://localhost:8080/sse")

        self.agent = Agent(
            model=model,
            name="Executive Briefing Assistant",
            tools=[self.mcp_handler],  # MCP provides email & calendar tools
            memory=self._create_memory(),
            reflection=True,
            # ... rest of config
        )

    def generate_briefing(self) -> MorningBriefing:
        task = Task(
            description="Fetch my unread emails and today's calendar, "
                        "then generate a morning briefing.",
            response_format=MorningBriefing,
            # No need to pass tools here — agent-level MCP tools are available
        )
        self.agent.do(task)
        return task.response
```

> **That's it!** The MCPHandler auto-discovers all tools from the MCP server. The agent will see `fetch_emails`, `get_calendar_events`, etc., and use them just like the simulated tools.

### Popular MCP Servers for This Agent

| Service | MCP Server | URL |
|---|---|---|
| Gmail + Calendar | google-workspace-mcp | [GitHub](https://github.com/nichochar/google-workspace-mcp) |
| Outlook + Calendar | microsoft-graph-mcp | [GitHub](https://github.com/microsoft/graph-mcp) |
| Slack | slack-mcp | [GitHub](https://github.com/anthropics/mcp-slack) |

## Powered By

- **Upsonic** v0.69.x — Agent framework
- **OpenAI** gpt-4o — Language model
- **Python** 3.10+
