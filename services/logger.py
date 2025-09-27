import os
import json
from datetime import datetime
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "credentials.json"  
SHEET_NAME = "GMTN Chat Logs"

# -------------------------------
# Lazy initialization
# -------------------------------
sheet = None

def init_sheet():
    global sheet
    if sheet is not None:
        return sheet

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    try:
        # Use Streamlit secrets if available
        creds_info = st.secrets.get("gcp_service_account")
        if creds_info:
            creds_json_str = json.dumps(creds_info)
            creds_file_path = "gcp_temp.json"
            with open(creds_file_path, "w") as f:
                f.write(creds_json_str)
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)
            os.remove(creds_file_path)
        else:
            raise ValueError("No Streamlit secrets, falling back to local JSON")

    except Exception:
        # fallback to local JSON
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"[Logger Warning] Local credentials file '{CREDENTIALS_FILE}' not found. Logging disabled.")
            return None
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)

    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

# -------------------------------
# Logging function
# -------------------------------
def log_chat(role: str, message: str):
    """
    Append a chat message to Google Sheets
    """
    global sheet
    if sheet is None:
        sheet = init_sheet()
        if sheet is None:
            print(f"[Logger Warning] Google Sheet not initialized. Skipping log.")
            return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        sheet.append_row([timestamp, role, message])
    except Exception as e:
        print(f"[Logger Error] Could not log to Google Sheets: {e}")
