# Google Sheets & Places API Setup

## Step 1 — Create a Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click "New Project" and give it a name (e.g. "Web Design Agents")
3. Select it as your active project

## Step 2 — Enable the APIs

1. In the left menu go to **APIs & Services > Library**
2. Search for and enable:
   - **Google Sheets API**
   - **Google Drive API**
   - **Places API**

## Step 3 — Create a Service Account (for Google Sheets)

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > Service Account**
3. Give it a name, click Done
4. Click the service account you just created
5. Go to the **Keys** tab > **Add Key > Create New Key > JSON**
6. Download the JSON file and save it as `credentials.json` in this project folder
7. Copy the `client_email` from the JSON file

## Step 4 — Share Your Google Sheet

1. Create a new Google Sheet at sheets.google.com
2. Click **Share** and paste the `client_email` from step 3 — give it **Editor** access
3. Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/THIS_PART_HERE/edit`
4. Paste it as `GOOGLE_SHEET_ID` in your `.env` file

## Step 5 — Get Your Places API Key

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > API Key**
3. Copy the key and paste it as `GOOGLE_PLACES_API_KEY` in your `.env` file
