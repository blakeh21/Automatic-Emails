import streamlit as st

# Initialize Streamlit and Gmail configurations
st.set_page_title("Email Tracker")
sidebar = st.sidebar
col1, col2, col3 = st.columns(3)

col1.header("Unread Emails/Follow Ups")
col1.write("""
         # Here are unread emails
         This would be email content""")

col2.header("Automation")
col1.write("""
         # Here are unread emails
         This would be email content""")

col3.header("Unread Emails")
col1.write("""
         # Here are unread emails
         This would be email content""")