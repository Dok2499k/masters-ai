import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pytz  # Library for handling time zones
import logging  # For logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Utility to get Google Calendar service
def get_calendar_service():
    token_file = 'token.json'
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        logging.info("Loaded credentials from token file.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logging.info("Refreshed expired credentials.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            logging.info("Generated new credentials using OAuth flow.")

        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            logging.info("Saved credentials to token file.")

    return build('calendar', 'v3', credentials=creds)

# Function to create an event
def create_event(summary, start_time_str, end_time_str, attendees=None, timezone=None):
    service = get_calendar_service()

    # Detect local timezone if none is provided
    if not timezone:
        local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        timezone = str(local_timezone)

    event_body = {
        'summary': summary,
        'start': {'dateTime': start_time_str, 'timeZone': timezone},
        'end': {'dateTime': end_time_str, 'timeZone': timezone},
        'attendees': [{'email': email} for email in (attendees or [])],
    }

    logging.info(f"Creating event: {event_body}")

    try:
        created_event = service.events().insert(calendarId='primary', body=event_body).execute()
        logging.info(f"Event created successfully: {created_event.get('htmlLink')}")
        return created_event.get('htmlLink', '')
    except Exception as e:
        logging.error(f"Error creating event: {e}")
        return f"Error creating event: {e}"

# Function to fetch events for a specific period
def get_events_for_period(start_time, end_time):
    service = get_calendar_service()
    try:
        logging.info(f"Fetching events from {start_time} to {end_time}.")
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_time.isoformat() + 'Z' if start_time.tzinfo is None or start_time.tzinfo.utcoffset(start_time) == datetime.timedelta(0) else start_time.isoformat(),
            timeMax=end_time.isoformat() + 'Z' if end_time.tzinfo is None or end_time.tzinfo.utcoffset(end_time) == datetime.timedelta(0) else end_time.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        logging.info(f"Fetched events: {events}")
        return events
    except Exception as e:
        logging.error(f"Error fetching events for the period: {e}")
        return f"Error fetching events for the period: {e}"
