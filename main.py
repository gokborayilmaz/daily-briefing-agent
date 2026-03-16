import os
import sys
from dotenv import load_dotenv

from agents.briefing_agent import ExecutiveBriefingAgent


def print_briefing(briefing):
    """Pretty-print the morning briefing."""
    print(f"\n{'=' * 60}")
    print(f"  {briefing.greeting}")
    print(f"  📅 {briefing.date}")
    print(f"{'=' * 60}")

    if briefing.urgent_emails:
        print(f"\n🔴 URGENT EMAILS ({len(briefing.urgent_emails)})")
        print("-" * 40)
        for email in briefing.urgent_emails:
            print(f"  📧 From: {email.sender}")
            print(f"     Subject: {email.subject}")
            print(f"     {email.snippet[:100]}...")
            print()

    if briefing.other_emails:
        print(f"\n📬 OTHER EMAILS ({len(briefing.other_emails)})")
        print("-" * 40)
        for email in briefing.other_emails:
            print(f"  📧 {email.sender} — {email.subject}")

    if briefing.today_schedule:
        print(f"\n📅 TODAY'S SCHEDULE ({len(briefing.today_schedule)})")
        print("-" * 40)
        for event in briefing.today_schedule:
            location = f" | 📍 {event.location}" if event.location else ""
            attendees = (
                f" | 👥 {', '.join(event.attendees)}"
                if event.attendees
                else ""
            )
            print(f"  ⏰ {event.start_time} - {event.end_time}")
            print(f"     {event.title}{location}{attendees}")
            print()

    if briefing.follow_ups:
        print(f"\n📌 FOLLOW-UPS ({len(briefing.follow_ups)})")
        print("-" * 40)
        for item in briefing.follow_ups:
            priority_icon = "🔴" if item.priority == "high" else "🟡"
            print(f"  {priority_icon} {item.contact} — {item.topic}")
            print(f"     Due: {item.due_date}")
            print()

    print(f"\n💡 SUMMARY")
    print("-" * 40)
    print(f"  {briefing.summary}")
    print(f"\n{'=' * 60}\n")


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment.")
        print("   Copy .env.example to .env and add your key.")
        sys.exit(1)

    print("☀️  Generating your morning briefing...\n")

    assistant = ExecutiveBriefingAgent()
    briefing = assistant.generate_briefing()
    print_briefing(briefing)

    # Interactive follow-up chat
    print("💬 Ask follow-up questions (type 'quit' to exit):\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Have a productive day. 👋")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! Have a productive day. 👋")
            break

        response = assistant.chat(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
