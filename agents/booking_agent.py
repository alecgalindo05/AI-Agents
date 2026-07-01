"""Booking Agent — converts interested leads into scheduled discovery calls."""
import os
import resend
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
from shared.db import get_interested_leads, create_booking, update_lead_status
from shared.claude_client import ask

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]
twilio = TwilioClient(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

CALENDLY_LINK = os.environ.get("CALENDLY_LINK", "https://calendly.com/yourlink")
BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "our web design team")

SYSTEM_PROMPT = """You write short, warm booking confirmation messages for a web design business.
Always include the scheduling link. Be concise and friendly."""


def generate_booking_message(business_name: str, channel: str) -> str:
    return ask(
        f"Write a {channel} message to '{business_name}' inviting them to book a free "
        f"discovery call. Include this link: {CALENDLY_LINK}",
        system=SYSTEM_PROMPT,
    )


def send_booking_email(lead: dict):
    message = generate_booking_message(lead["business_name"], "email")
    resend.Emails.send({
        "from": os.environ["FROM_EMAIL"],
        "to": lead["email"],
        "subject": f"Let's find a time to chat about your website!",
        "text": message,
    })


def send_booking_sms(lead: dict):
    message = generate_booking_message(lead["business_name"], "SMS")
    twilio.messages.create(
        body=message,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        to=lead["phone"],
    )


def process_interested_leads():
    """Check for interested leads and send them booking invitations."""
    leads = get_interested_leads()
    print(f"Found {len(leads)} interested leads")

    for lead in leads:
        if lead.get("email"):
            send_booking_email(lead)
        elif lead.get("phone"):
            send_booking_sms(lead)
        update_lead_status(lead["id"], "booking_sent")
        print(f"Sent booking invite to {lead['business_name']}")


def confirm_booking(lead_id: str, scheduled_at: str):
    """Record a confirmed booking once a lead picks a time."""
    booking = create_booking(lead_id, scheduled_at)
    print(f"Booking confirmed: {booking['id']} at {scheduled_at}")
    return booking


if __name__ == "__main__":
    process_interested_leads()
