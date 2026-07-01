import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None

def get_db() -> Client:
    global _client
    if _client is None:
        _client = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"],
        )
    return _client

def add_lead(name: str, business_name: str = None, email: str = None,
             phone: str = None, social_handle: str = None, source: str = None) -> dict:
    db = get_db()
    result = db.table("leads").insert({
        "name": name,
        "business_name": business_name,
        "email": email,
        "phone": phone,
        "social_handle": social_handle,
        "source": source,
        "status": "new",
    }).execute()
    return result.data[0]

def update_lead_status(lead_id: str, status: str, notes: str = None):
    db = get_db()
    payload = {"status": status, "updated_at": "NOW()"}
    if notes:
        payload["notes"] = notes
    db.table("leads").update(payload).eq("id", lead_id).execute()

def log_outreach(lead_id: str, channel: str, message: str):
    db = get_db()
    db.table("outreach_log").insert({
        "lead_id": lead_id,
        "channel": channel,
        "message": message,
    }).execute()

def log_response(outreach_id: str, response: str):
    db = get_db()
    db.table("outreach_log").update({
        "response": response,
        "responded_at": "NOW()",
    }).eq("id", outreach_id).execute()

def create_booking(lead_id: str, scheduled_at: str) -> dict:
    db = get_db()
    result = db.table("bookings").insert({
        "lead_id": lead_id,
        "scheduled_at": scheduled_at,
        "status": "scheduled",
    }).execute()
    update_lead_status(lead_id, "booked")
    return result.data[0]

def get_interested_leads() -> list:
    db = get_db()
    result = db.table("leads").select("*").eq("status", "interested").execute()
    return result.data

def get_stats_summary() -> dict:
    db = get_db()
    leads = db.table("leads").select("status", count="exact").execute()
    bookings = db.table("bookings").select("deal_value").eq("status", "completed").execute()
    outreach = db.table("outreach_log").select("channel", count="exact").execute()

    total_revenue = sum(b["deal_value"] or 0 for b in bookings.data)
    return {
        "total_leads": leads.count,
        "total_revenue": total_revenue,
        "outreach_sent": outreach.count,
        "bookings": len(bookings.data),
    }
