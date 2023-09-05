# Import necessary libraries
import streamlit as st
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize Streamlit and Gmail configurations
st.set_page_title("Email Tracker")
sidebar = st.sidebar
col1, col2, col3 = st.beta_columns(3)

# Authenticate and access Gmail
creds, _ = google.auth.default()
gmail_service = build('gmail', 'v1', credentials=creds)

# Retrieve unread emails
results = gmail_service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
messages = results.get('messages', [])

# Display unread emails
col1.header("Unread Emails")
for message in messages:
    msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
    col1.write(msg['snippet'])

# Access Google Sheets for client emails
sheets_service = build('sheets', 'v4', credentials=creds)
sheet_id = 'YOUR_SHEET_ID'
range_name = 'A1:B100' # Assuming emails are in column A
sheet_data = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
client_emails = [row[0] for row in sheet_data.get('values', [])]

# Prioritize client emails
for message in messages:
    msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
    email_address = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'][0]
    if email_address in client_emails:
        col1.markdown(f"**{msg['snippet']}**") # Highlighting client email

# Response tracking
col3.header("Response Reminders")
for message in messages:
    msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
    received_time = int(msg['internalDate'])
    current_time = st.time()
    if (current_time - received_time) > 604800000: # 7 days in milliseconds
        col3.write(f"Reminder: Respond to {msg['snippet']}")

