# Web Design Multi-Agent System

Three AI agents that work together to grow your web design business:

- **Outreach Agent** — Finds leads and contacts them via email, SMS, and social DMs
- **Booking Agent** — Converts interested leads into booked discovery calls
- **Analytics Agent** — Tracks everything and surfaces insights

All agents share a single Supabase database and are powered by Claude AI.

## Structure

```
agents/
  outreach_agent.py     # Lead outreach via email/SMS/DM
  booking_agent.py      # Scheduling and confirmations
  analytics_agent.py    # Stats, reporting, insights
shared/
  db.py                 # Shared database client
  claude_client.py      # Shared Claude API client
database/
  schema.sql            # Full database schema
.env.example            # Required environment variables
requirements.txt
```

## Setup

1. Create a [Supabase](https://supabase.com) project (free)
2. Run `database/schema.sql` in the Supabase SQL editor
3. Copy `.env.example` to `.env` and fill in your keys
4. `pip install -r requirements.txt`
5. Run any agent: `python agents/outreach_agent.py`
