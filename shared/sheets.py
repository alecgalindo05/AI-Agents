import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

LEADS_HEADERS = [
    "Business Name", "City", "State", "Industry", "Phone",
    "Website URL", "Website Status", "Outdated Reasons",
    "Template Used", "Message Sent", "Date Contacted",
    "Response", "Response Date", "Notes",
]

_sheet = None


def get_sheet():
    global _sheet
    if _sheet is None:
        creds = Credentials.from_service_account_file(
            os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"], scopes=SCOPES
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])

        try:
            _sheet = spreadsheet.worksheet("Leads")
        except gspread.WorksheetNotFound:
            _sheet = spreadsheet.add_worksheet(title="Leads", rows=1000, cols=20)
            _sheet.append_row(LEADS_HEADERS)

    return _sheet


def log_lead(lead: dict, message: str, channel: str | None):
    sheet = get_sheet()
    sheet.append_row([
        lead.get("business_name", ""),
        lead.get("city", ""),
        lead.get("state", ""),
        lead.get("industry", ""),
        lead.get("phone", ""),
        lead.get("website_url", ""),
        lead.get("website_status", ""),
        lead.get("outdated_reasons", ""),
        lead.get("template_used", ""),
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",  # Response (filled in manually)
        "",  # Response Date
        "",  # Notes
    ])


def get_all_leads() -> list[dict]:
    sheet = get_sheet()
    rows = sheet.get_all_records()
    return rows
