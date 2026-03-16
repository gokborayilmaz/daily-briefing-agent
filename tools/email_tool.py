import json
from datetime import datetime, timedelta


def fetch_unread_emails() -> str:
    """Fetch all unread emails from the user's inbox.

    Returns a JSON list of unread emails with sender, subject,
    snippet, urgency flag, and received timestamp.
    """
    now = datetime.now()

    emails = [
        {
            "sender": "Sarah Chen <sarah.chen@techcorp.com>",
            "subject": "URGENT: Q1 Revenue Numbers Need Your Sign-Off",
            "snippet": "Hi, the finance team needs your approval on the Q1 revenue report by noon today. The board presentation is tomorrow and we can't proceed without your sign-off. Key figures attached.",
            "is_urgent": True,
            "received_at": (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "James Rodriguez <james.r@clientpartners.io>",
            "subject": "RE: Partnership Proposal - Action Required",
            "snippet": "Following up on our call last week. We'd love to move forward with the strategic partnership. Can you confirm the terms we discussed? Our legal team is ready to draft the agreement.",
            "is_urgent": True,
            "received_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "HR Department <hr@company.com>",
            "subject": "New PTO Policy Update - Effective April 1st",
            "snippet": "Please review the updated PTO policy attached. Key changes include increased carryover days and a new sabbatical program for employees with 5+ years tenure.",
            "is_urgent": False,
            "received_at": (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "Mike Thompson <mike.t@engineering.internal>",
            "subject": "Sprint Retrospective Notes + Action Items",
            "snippet": "Attached are the retro notes from yesterday. Main takeaway: we need to address the deployment pipeline bottleneck. I've drafted a proposal for your review.",
            "is_urgent": False,
            "received_at": (now - timedelta(hours=7)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "Priya Sharma <priya@analytics.co>",
            "subject": "Customer Churn Analysis - Concerning Trends",
            "snippet": "Our latest analysis shows a 12% increase in churn among enterprise customers this quarter. I've identified three key drivers and have recommendations ready to discuss.",
            "is_urgent": True,
            "received_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "LinkedIn <notifications@linkedin.com>",
            "subject": "5 people viewed your profile this week",
            "snippet": "See who's been looking at your profile and discover new connection opportunities.",
            "is_urgent": False,
            "received_at": (now - timedelta(hours=10)).strftime("%Y-%m-%d %H:%M"),
        },
        {
            "sender": "David Park <david.p@legal.internal>",
            "subject": "Contract Review: Vendor Agreement #4521",
            "snippet": "I've completed the legal review of the vendor agreement. There are two clauses that need revision before we can proceed. Summary of changes attached.",
            "is_urgent": False,
            "received_at": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
        },
    ]

    return json.dumps(emails, indent=2)
