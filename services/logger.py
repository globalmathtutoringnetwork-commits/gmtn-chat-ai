import os
import json
from datetime import datetime
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# Configuration
# -------------------------------
LOCAL_CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "GMTN Chat Logs"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# -------------------------------
# Lazy initialization
# -------------------------------
sheet = None

def init_sheet():
    """
    Initialize and return the Google Sheet object.
    Works with local JSON file or Streamlit secrets.
    """
    global sheet
    if sheet is not None:
        return sheet

    creds = None

    # First, try Streamlit secrets (deployed)
    try:
        creds_info = st.secrets.get("gcp_service_account")
        if creds_info:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, SCOPE)
    except Exception as e:
        print(f"[Logger Warning] Failed to use Streamlit secrets: {e}")

    # Fallback to local JSON (development)
    if creds is None:
        if os.path.exists(LOCAL_CREDENTIALS_FILE):
            try:
                creds = ServiceAccountCredentials.from_json_keyfile_name(LOCAL_CREDENTIALS_FILE, SCOPE)
            except Exception as e:
                print(f"[Logger Warning] Failed to use local credentials: {e}")
        else:
            print(f"[Logger Warning] Local credentials file '{LOCAL_CREDENTIALS_FILE}' not found.")

    if creds is None:
        print("[Logger Error] No valid credentials found. Google Sheet logging disabled.")
        return None

    try:
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
    except Exception as e:
        print(f"[Logger Error] Could not connect to Google Sheet '{SHEET_NAME}': {e}")
        return None

    return sheet

# -------------------------------
# Logging function
# -------------------------------
def log_chat(role: str, message: str):
    """
    Append a chat message to Google Sheets.
    """
    global sheet
    if sheet is None:
        sheet = init_sheet()
        if sheet is None:
            print("[Logger Warning] Sheet not initialized. Skipping log.")
            return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        sheet.append_row([timestamp, role, message])
    except Exception as e:
        print(f"[Logger Error] Could not append row to Google Sheet: {e}")
