-- Leads: everyone Agent 1 has found or contacted
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  business_name TEXT,
  email TEXT,
  phone TEXT,
  social_handle TEXT,
  source TEXT,                        -- 'email' | 'sms' | 'instagram' | 'facebook'
  status TEXT DEFAULT 'new',          -- 'new' | 'contacted' | 'interested' | 'booked' | 'closed' | 'lost'
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Outreach: every message sent to a lead
CREATE TABLE IF NOT EXISTS outreach_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id),
  channel TEXT NOT NULL,              -- 'email' | 'sms' | 'dm'
  message TEXT NOT NULL,
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  response TEXT,
  responded_at TIMESTAMPTZ
);

-- Bookings: discovery calls booked by Agent 2
CREATE TABLE IF NOT EXISTS bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id),
  scheduled_at TIMESTAMPTZ NOT NULL,
  status TEXT DEFAULT 'scheduled',    -- 'scheduled' | 'completed' | 'no_show' | 'cancelled'
  outcome TEXT,                       -- 'closed' | 'follow_up' | 'not_interested'
  deal_value NUMERIC(10,2),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Daily stats snapshot for analytics
CREATE TABLE IF NOT EXISTS daily_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE UNIQUE NOT NULL DEFAULT CURRENT_DATE,
  leads_added INT DEFAULT 0,
  messages_sent INT DEFAULT 0,
  responses_received INT DEFAULT 0,
  bookings_made INT DEFAULT 0,
  deals_closed INT DEFAULT 0,
  revenue NUMERIC(10,2) DEFAULT 0
);
