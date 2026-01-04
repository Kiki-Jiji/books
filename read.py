import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Path to your service account JSON
SERVICE_ACCOUNT_FILE = "my-service-account.json"

# Required scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Authenticate
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
client = gspread.authorize(creds)

# Open sheet (by name or URL)
sheet = client.open("My Google Sheet").sheet1
# OR: client.open_by_url("https://docs.google.com/spreadsheets/d/...")
# OR: client.open_by_key("SHEET_ID")

# Get all values
data = sheet.get_all_records()

# Load into pandas
df = pd.DataFrame(data)

print(df.head())
