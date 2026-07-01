import os
import resend
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ.get("RESEND_API_KEY", "")


def send_sms(to: str, message: str) -> bool:
    twilio = TwilioClient(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"],
    )
    twilio.messages.create(
        body=message,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        to=to,
    )
    return True


def send_email(to: str, subject: str, body: str) -> bool:
    resend.Emails.send({
        "from": os.environ["FROM_EMAIL"],
        "to": to,
        "subject": subject,
        "text": body,
    })
    return True


def email_yourself(subject: str, body: str):
    send_email(os.environ["YOUR_EMAIL"], subject, body)
