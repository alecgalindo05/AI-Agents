"""Outreach Agent — finds leads, detects website status, and sends personalized messages."""
import os
import time
import argparse
import googlemaps
from dotenv import load_dotenv
from shared.website_checker import classify_website
from shared.sheets import log_lead
from shared.mailer import send_sms

load_dotenv()


def load_template(name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "..", "templates", f"{name}.txt")
    with open(os.path.normpath(path)) as f:
        return f.read().strip()


def personalize(template: str, lead: dict) -> str:
    return (
        template
        .replace("{company_name}", lead.get("business_name", ""))
        .replace("{city}", lead.get("city", ""))
        .replace("{state}", lead.get("state", ""))
        .replace("{industry}", lead.get("industry", ""))
    )


def find_leads(business_type: str, city: str, state: str, max_results: int = 20) -> list:
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_PLACES_API_KEY"])
    results = gmaps.places(query=f"{business_type} in {city}, {state}")
    leads = []

    for place in results.get("results", [])[:max_results]:
        details = gmaps.place(
            place["place_id"],
            fields=["name", "formatted_phone_number", "website"]
        )["result"]

        website = details.get("website")
        site_info = classify_website(website)

        if site_info["status"] == "modern":
            continue

        leads.append({
            "business_name": details.get("name", ""),
            "city": city,
            "state": state,
            "industry": business_type,
            "phone": details.get("formatted_phone_number", ""),
            "website_url": website or "",
            "website_status": site_info["status"],
            "outdated_reasons": ", ".join(site_info["reasons"]),
        })
        time.sleep(0.2)

    return leads


def run(business_type: str, city: str, state: str):
    template_no_site = load_template("no_website")
    template_outdated = load_template("outdated_website")

    leads = find_leads(business_type, city, state)
    print(f"Found {len(leads)} leads in {city}, {state}")

    for lead in leads:
        if lead["website_status"] == "none":
            template = template_no_site
            template_used = "no_website"
        else:
            template = template_outdated
            template_used = "outdated_website"

        message = personalize(template, lead)
        lead["template_used"] = template_used

        sent_via = None
        if lead.get("phone"):
            send_sms(lead["phone"], message)
            sent_via = "sms"

        log_lead(lead, message, sent_via)
        print(f"  Contacted {lead['business_name']} via {sent_via or 'not sent — no contact info'}")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, help="Business type, e.g. 'restaurant'")
    parser.add_argument("--city", required=True, help="City to search in")
    parser.add_argument("--state", required=True, help="State, e.g. TX")
    args = parser.parse_args()
    run(args.type, args.city, args.state)
