import os
import json
import datetime
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from google_calendar import create_event, get_events_for_period
import logging  # For logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utility function to initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful calendar assistant."}
        ]
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

# Function to render chat messages
def render_messages():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['content']}")

# Function to handle user input and OpenAI response
def handle_user_input(client):
    user_input = st.text_input(
        "Enter your message:",
        value=st.session_state.user_input,
        key="user_input_field"
    )

    if st.button("Send"):
        if user_input.strip():
            logging.info(f"User input received: {user_input}")
            # Append user message to the session state
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Call OpenAI API
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                functions=[
                    {
                        "name": "create_calendar_event",
                        "description": "Create a new Google Calendar event",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "summary": {"type": "string", "description": "Title of the event"},
                                "start_time": {"type": "string", "description": "Event start time in ISO 8601 format"},
                                "end_time": {"type": "string", "description": "Event end time in ISO 8601 format"},
                                "attendees": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Optional list of attendee email addresses"
                                }
                            },
                            "required": ["summary", "start_time", "end_time"]
                        }
                    },
                    {
                        "name": "fetch_calendar_events",
                        "description": "Fetch Google Calendar events for a specified period",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "start_time": {"type": "string", "description": "Start time in ISO 8601 format"},
                                "end_time": {"type": "string", "description": "End time in ISO 8601 format"}
                            },
                            "required": ["start_time", "end_time"]
                        }
                    }
                ],
                function_call="auto"
            )

            response_message = completion.choices[0].message

            # Handle function call
            if response_message.function_call:
                args = json.loads(response_message.function_call.arguments)
                if response_message.function_call.name == "create_calendar_event":
                    logging.info(f"Function call to create event: {args}")
                    result = create_event(
                        summary=args.get("summary"),
                        start_time_str=args.get("start_time"),
                        end_time_str=args.get("end_time"),
                        attendees=args.get("attendees", [])
                    )
                    st.session_state.messages.append({"role": "assistant", "content": result})
                elif response_message.function_call.name == "fetch_calendar_events":
                    logging.info(f"Function call to fetch events: {args}")
                    start_time = datetime.datetime.fromisoformat(args["start_time"])
                    end_time = datetime.datetime.fromisoformat(args["end_time"])
                    events = get_events_for_period(start_time, end_time)
                    if not events:
                        response_content = f"No events found from {start_time.date()} to {end_time.date()}."
                    else:
                        response_content = f"Events from {start_time.date()} to {end_time.date()}:\n"
                        for event in events:
                            if isinstance(event, dict):
                                event_start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
                                event_summary = event.get('summary', 'No Title')
                                response_content += f"- {event_start}: {event_summary}\n"
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
            else:
                # Handle plain response
                st.session_state.messages.append({"role": "assistant", "content": response_message.content})

            st.session_state.user_input = ""
            st.rerun()

# Main function
def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    initialize_session_state()

    st.title("Calendar Assistant")
    st.subheader("Chat History")
    render_messages()

    st.subheader("New Message")
    handle_user_input(client)

if __name__ == "__main__":
    main()
