"""Outreach Agent — finds leads and contacts them via email, SMS, or DM."""
import os
import resend
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
from shared.db import add_lead, log_outreach, update_lead_status
from shared.claude_client import ask

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]
twilio = TwilioClient(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

SYSTEM_PROMPT = """You are an outreach specialist for a web design business.
Write short, friendly, personalized messages that feel human — not spammy.
Focus on the value of a great website for their specific business.
Keep emails under 150 words. Keep SMS under 50 words."""


def generate_message(business_name: str, channel: str) -> str:
    return ask(
        f"Write a {channel} outreach message to '{business_name}' offering web design services.",
        system=SYSTEM_PROMPT,
    )


def send_email(lead: dict) -> bool:
    message = generate_message(lead["business_name"], "email")
    resend.Emails.send({
        "from": os.environ["FROM_EMAIL"],
        "to": lead["email"],
        "subject": f"Quick question about {lead['business_name']}'s website",
        "text": message,
    })
    log_outreach(lead["id"], "email", message)
    return True


def send_sms(lead: dict) -> bool:
    message = generate_message(lead["business_name"], "SMS")
    twilio.messages.create(
        body=message,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        to=lead["phone"],
    )
    log_outreach(lead["id"], "sms", message)
    return True


def contact_lead(name: str, business_name: str, email: str = None,
                 phone: str = None, social_handle: str = None):
    """Add a lead and contact them on all available channels."""
    source = "email" if email else ("sms" if phone else "dm")
    lead = add_lead(name, business_name, email, phone, social_handle, source)

    if email:
        send_email(lead)
    if phone:
        send_sms(lead)

    update_lead_status(lead["id"], "contacted")
    print(f"Contacted {business_name} via {source}")
    return lead


if __name__ == "__main__":
    # Example usage
    contact_lead(
        name="Jane Smith",
        business_name="Jane's Bakery",
        email="jane@janesbakery.com",
        phone="+15551234567",
    )
