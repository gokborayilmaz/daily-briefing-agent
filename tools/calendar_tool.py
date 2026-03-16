import json
from datetime import datetime, timedelta


def fetch_todays_calendar() -> str:
    """Fetch today's calendar events for the user.

    Returns a JSON list of today's meetings and events with
    title, start/end times, location, and attendees.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    events = [
        {
            "title": "Morning Stand-up",
            "start_time": f"{today} 09:00",
            "end_time": f"{today} 09:15",
            "location": "Zoom - Daily Room",
            "attendees": ["Engineering Team"],
        },
        {
            "title": "Q1 Revenue Review with Finance",
            "start_time": f"{today} 10:00",
            "end_time": f"{today} 11:00",
            "location": "Conference Room A",
            "attendees": [
                "Sarah Chen",
                "CFO Rachel Kim",
                "VP Finance Tom Liu",
            ],
        },
        {
            "title": "1:1 with Direct Report - Mike Thompson",
            "start_time": f"{today} 11:30",
            "end_time": f"{today} 12:00",
            "location": "Office",
            "attendees": ["Mike Thompson"],
        },
        {
            "title": "Lunch with James Rodriguez (Client Partners)",
            "start_time": f"{today} 12:30",
            "end_time": f"{today} 13:30",
            "location": "The Capital Grille - Downtown",
            "attendees": ["James Rodriguez"],
        },
        {
            "title": "Product Strategy Workshop",
            "start_time": f"{today} 14:00",
            "end_time": f"{today} 15:30",
            "location": "Innovation Lab",
            "attendees": [
                "Product Team",
                "Design Lead Amy",
                "CTO",
            ],
        },
        {
            "title": "Customer Churn Deep-Dive",
            "start_time": f"{today} 16:00",
            "end_time": f"{today} 16:45",
            "location": "Zoom",
            "attendees": ["Priya Sharma", "Analytics Team"],
        },
    ]

    return json.dumps(events, indent=2)
