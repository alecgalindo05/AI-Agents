# Web Design Lead & Analytics Agent System

Two AI agents that work together to grow your web design business.

## How It Works

**Agent 1 — Outreach Agent**
- Searches for businesses (by type + city) using Google Places
- Checks each business's website: none, outdated, or modern
- Skips businesses with modern websites
- Picks your template (no website vs outdated website)
- Fills in `{company_name}`, `{city}`, `{state}`, `{industry}` automatically
- Sends the message via SMS
- Logs every lead to your Google Sheet

**Agent 2 — Analytics Agent**
- Reads your Google Sheet and calculates key stats
- Sends you a weekly email digest
- Flags recommendations (e.g. "Template B has a low response rate") and emails you for approval before changing anything

## Your Message Templates

Edit these two files to control exactly what gets sent:

- `templates/no_website.txt` — sent to businesses with no website
- `templates/outdated_website.txt` — sent to businesses with an outdated website

Available placeholders:
- `{company_name}` — the business name
- `{city}` — city
- `{state}` — state
- `{industry}` — type of business (e.g. restaurant, salon)

## Google Sheet Structure

Your sheet will have these columns (auto-created on first run):

| Business Name | City | State | Industry | Phone | Website | Website Status | Outdated Reasons | Template Used | Message Sent | Date Contacted | Response | Response Date | Notes |

## Setup

1. **Google Sheet** — Create a new Google Sheet and note the Sheet ID from the URL
2. **Google Service Account** — Follow `docs/google_setup.md` to get credentials
3. **Twilio** — Sign up at twilio.com for SMS (free trial available)
4. **Resend** — Sign up at resend.com for email reports (free tier available)
5. **Anthropic** — Get your API key at console.anthropic.com
6. **Google Places** — Enable the Places API in Google Cloud Console
7. Copy `.env.example` to `.env` and fill in all values
8. `pip install -r requirements.txt`

## Running the Agents

```bash
# Run outreach for a specific search
python agents/outreach_agent.py --type "restaurant" --city "Austin" --state "TX"

# Run analytics report manually
python agents/analytics_agent.py
```
