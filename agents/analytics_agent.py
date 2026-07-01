"""Analytics Agent — tracks stats and surfaces insights to improve outreach and booking."""
from shared.db import get_db, get_stats_summary
from shared.claude_client import ask

SYSTEM_PROMPT = """You are a business analyst for a web design agency.
Given raw stats, provide a short (3-5 bullet) plain-English summary with
actionable recommendations. Be direct and specific."""


def get_channel_breakdown() -> dict:
    db = get_db()
    rows = db.table("outreach_log").select("channel").execute()
    breakdown = {}
    for row in rows.data:
        ch = row["channel"]
        breakdown[ch] = breakdown.get(ch, 0) + 1
    return breakdown


def get_conversion_rate() -> float:
    db = get_db()
    total = db.table("leads").select("id", count="exact").execute().count
    booked = db.table("leads").select("id", count="exact").eq("status", "booked").execute().count
    return round((booked / total * 100), 1) if total else 0.0


def generate_report() -> str:
    summary = get_stats_summary()
    channels = get_channel_breakdown()
    conversion = get_conversion_rate()

    stats_text = (
        f"Total leads: {summary['total_leads']}\n"
        f"Outreach sent: {summary['outreach_sent']}\n"
        f"Bookings: {summary['bookings']}\n"
        f"Conversion rate: {conversion}%\n"
        f"Total revenue: ${summary['total_revenue']:,.2f}\n"
        f"Channel breakdown: {channels}"
    )

    insights = ask(
        f"Here are my web design business stats:\n{stats_text}\n\nGive me a brief analysis.",
        system=SYSTEM_PROMPT,
    )

    report = f"=== Analytics Report ===\n{stats_text}\n\n=== Insights ===\n{insights}"
    print(report)
    return report


if __name__ == "__main__":
    generate_report()
