"""Analytics Agent — tracks stats, sends weekly reports, and flags recommendations for your approval."""
import os
from collections import Counter
from dotenv import load_dotenv
from shared.sheets import get_all_leads
from shared.claude_client import ask
from shared.mailer import email_yourself

load_dotenv()

BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "your business")

ANALYST_SYSTEM = """You are a sharp business analyst for a web design agency.
Given lead and outreach data, write a concise report:
- 3-5 bullet points on what's working and what isn't
- 1-2 specific, actionable recommendations
- Flag anything that needs the owner's attention
Be direct. No fluff."""


def compute_stats(leads: list[dict]) -> dict:
    total = len(leads)
    responded = sum(1 for l in leads if l.get("Response"))
    by_template = Counter(l.get("Template Used") for l in leads if l.get("Template Used"))
    by_channel = Counter(l.get("Channel") for l in leads if l.get("Channel"))

    response_by_template = {}
    for template in by_template:
        group = [l for l in leads if l.get("Template Used") == template]
        resp = sum(1 for l in group if l.get("Response"))
        rate = round(resp / len(group) * 100, 1) if group else 0
        response_by_template[template] = {"sent": len(group), "response_rate": rate}

    return {
        "total_leads": total,
        "total_responses": responded,
        "overall_response_rate": round(responded / total * 100, 1) if total else 0,
        "by_template": response_by_template,
        "by_channel": dict(by_channel),
    }


def build_report_text(stats: dict) -> str:
    lines = [
        f"Total leads contacted: {stats['total_leads']}",
        f"Total responses: {stats['total_responses']}",
        f"Overall response rate: {stats['overall_response_rate']}%",
        "\nBy template:",
    ]
    for template, data in stats["by_template"].items():
        lines.append(f"  {template}: {data['sent']} sent, {data['response_rate']}% response rate")
    lines.append("\nBy channel:")
    for channel, count in stats["by_channel"].items():
        lines.append(f"  {channel}: {count} messages")
    return "\n".join(lines)


def check_for_recommendations(stats: dict) -> list[str]:
    """Returns a list of issues that need owner approval before acting on."""
    flags = []
    for template, data in stats["by_template"].items():
        if data["sent"] >= 10 and data["response_rate"] < 5:
            flags.append(
                f"Template '{template}' has only a {data['response_rate']}% response rate "
                f"after {data['sent']} messages. Consider rewriting it. "
                f"Reply YES to have me draft a new version for your review."
            )
    return flags


def run():
    leads = get_all_leads()
    if not leads:
        print("No leads found in sheet yet.")
        return

    stats = compute_stats(leads)
    report_text = build_report_text(stats)

    ai_insights = ask(
        f"Here are the outreach stats for {BUSINESS_NAME}:\n{report_text}\n\nProvide your analysis.",
        system=ANALYST_SYSTEM,
    )

    full_report = (
        f"=== Weekly Report: {BUSINESS_NAME} ===\n\n"
        f"{report_text}\n\n"
        f"=== AI Insights ===\n{ai_insights}"
    )

    print(full_report)
    email_yourself(
        subject=f"Weekly Outreach Report — {BUSINESS_NAME}",
        body=full_report,
    )
    print("Report emailed to you.")

    recommendations = check_for_recommendations(stats)
    for rec in recommendations:
        email_yourself(
            subject=f"Recommendation from Analytics Agent — {BUSINESS_NAME}",
            body=(
                f"Your analytics agent spotted something and wants your approval before acting:\n\n"
                f"{rec}\n\n"
                f"Reply to this email to let me know how you'd like to proceed."
            ),
        )
        print(f"Recommendation emailed: {rec[:80]}...")


if __name__ == "__main__":
    run()
