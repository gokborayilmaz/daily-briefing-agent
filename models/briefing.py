from typing import List, Optional
from pydantic import BaseModel, Field


class Email(BaseModel):
    sender: str
    subject: str
    snippet: str
    is_urgent: bool = False
    received_at: str


class CalendarEvent(BaseModel):
    title: str
    start_time: str
    end_time: str
    location: Optional[str] = None
    attendees: List[str] = Field(default_factory=list)


class FollowUp(BaseModel):
    contact: str
    topic: str
    due_date: str
    priority: str = "normal"


class MorningBriefing(BaseModel):
    greeting: str
    date: str
    urgent_emails: List[Email] = Field(default_factory=list)
    other_emails: List[Email] = Field(default_factory=list)
    today_schedule: List[CalendarEvent] = Field(default_factory=list)
    follow_ups: List[FollowUp] = Field(default_factory=list)
    summary: str
