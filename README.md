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
| **Default Model** | `openai/gpt-4o` |
| **Memory** | SQLite (`full_session_memory=True`) |
| **Reflection** | Enabled (urgency re-evaluation) |
| **Safety** | AgentPolicy (PII anonymization) |

## Installation

### Clone Repostrory
```bash
git clone https://github.com/gokborayilmaz/executive-daily-briefing-agent.git
cd ------
```
### Create Virtual Environment
```bash
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate   # macOS/Linux
```
### Install Dependencies
```bash
uv pip install -r requirements.txt
```
### Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and Google API Keys
```

## Usage 
You can chat with this agent via the CLI or through the Streamlit UI. Whichever one you want to use, run it.

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
| `USER_NAME` | `Bora` | Executive's name (used in prompts) |
| `USER_TIMEZONE` | `US/Eastern` | Timezone for scheduling |

## Connecting Real Email & Calendar via MCP

The simulated tools in `tools/` can be replaced with real MCP (Model Context Protocol) integrations in two simple steps:

### Step 1 — Install an MCP Server

For **Gmail + Google Calendar**, use the [Google Workspace MCP Server](https://github.com/nichochar/google-workspace-mcp):

```bash
# Install the MCP server
pip install google-workspace-mcp
```

### Step 2 — Connect to the Agent

Replace the tools with MCP tools in `agents/briefing_agent.py`:

```python
    def generate_briefing(self) -> MorningBriefing:
        """It returns a structured summary by scanning emails and the calendar"""
        briefing_task = Task(
            f"Generate today's morning briefing for {USER_NAME}.",
            # Use this tools line for MCP connection
          # tools= [GoogleWorkspaceMCP]
            # Use this tools line for Quick try
            tools=[fetch_unread_emails, fetch_todays_calendar], 
            response_format=MorningBriefing
        )
        self.agent.do(briefing_task)
        return briefing_task.response
```

> **That's it!** The MCPHandler auto-discovers all tools from the MCP server. The agent will see `fetch_emails`, `get_calendar_events`, etc., and use them just like the simulated tools.

## Powered By

- **Upsonic** v0.73.2 — Agent framework
- **OpenAI** gpt-4o — Language model
- **Python** 3.10+
