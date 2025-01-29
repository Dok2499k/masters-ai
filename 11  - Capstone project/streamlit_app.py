import os
import io
import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from google_calendar import create_event
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utility function to initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant who integrates calendar and database functionalities."}
        ]
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

# Query the database and return results
def ask_database(query):
    conn = sqlite3.connect('db/employee_data.db')
    logging.info(f"Executing query: {query}")
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        return f"Error querying database: {e}"

# Get employee status distribution
# For hardcoded sidebar with distribution to decorate the application
def get_employee_status_distribution():
    conn = sqlite3.connect('db/employee_data.db')
    try:
        query = """
        SELECT EmployeeStatus, COUNT(*) as Count
        FROM employee_data
        GROUP BY EmployeeStatus
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        logging.error(f"Error fetching employee status distribution: {e}")
        return None

def get_employee_type_distribution():
    conn = sqlite3.connect('db/employee_data.db')
    try:
        query = """
        SELECT EmployeeType, COUNT(*) as Count
        FROM employee_data
        GROUP BY EmployeeType
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        logging.error(f"Error fetching employee type distribution: {e}")
        return None

# Visualize data using Streamlit
def visualize_data(data, chart_type):
    try:
        df = pd.read_csv(io.StringIO(data))

        if chart_type == "bar":
            st.bar_chart(df.set_index(df.columns[0]))
        elif chart_type == "line":
            st.line_chart(df.set_index(df.columns[0]))
        elif chart_type == "pie":
            fig, ax = plt.subplots()
            ax.pie(df[df.columns[1]], labels=df[df.columns[0]], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Ensures the pie chart is a circle

            # **This ensures the pie chart actually renders in Streamlit**
            st.pyplot(fig)
        elif chart_type == "table":
            st.dataframe(df)
        else:
            st.write(f"Unknown chart type: {chart_type}")

    except Exception as e:
        logging.error(f"Error visualizing data: {e}")
        st.write(f"Error visualizing data: {e}")

# Display employee status chart
# For hardcoded sidebar with distribution to decorate the application
def display_employee_status_chart():
    st.subheader("Current Employee Status Distribution in Company")

    # Fetch the data
    df = get_employee_status_distribution()

    if df is not None and not df.empty:
        # Create the bar chart
        st.bar_chart(data=df.set_index('EmployeeStatus'))
    else:
        st.write("No data available to display the employee status distribution.")

# Display employee type pie chart
# For hardcoded sidebar with distribution to decorate the application
def display_employee_type_chart():
    st.subheader("Current Employee Type Distribution in Company")
    df = get_employee_type_distribution()
    if df is not None and not df.empty:
        fig, ax = plt.subplots()
        ax.pie(df["Count"], labels=df["EmployeeType"], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.write("No data available to display the employee type distribution.")


# Render chat messages
def render_messages():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['content']}" )

# Handle user input and OpenAI response
def handle_user_input(client):
    user_input = st.text_input(
        "Enter your message:",
        value=st.session_state.user_input,
        key="user_input_field"
    )

    if st.button("Send"):
        if user_input.strip():
            logging.info(f"User input received: {user_input}")
            logging.info(f"Session state: {st.session_state}")

            st.session_state.messages.append({"role": "user", "content": user_input})

            # **Modify available functions based on session state**
            functions = [
                {
                    "name": "visualize_data",
                    "description": "Generate a chart or table in Streamlit",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {"type": "string", "description": "Data in CSV format"},
                            "chart_type": {
                                "type": "string",
                                "enum": ["bar", "line", "pie", "table"],
                                "description": "Type of chart or visualization"
                            }
                        },
                        "required": ["data", "chart_type"]
                    }
                },
                {
                    "name": "create_calendar_event",
                    "description": "Create a new Google Calendar event",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "Title of the event"},
                            "start_time": {"type": "string", "description": "Event start time in ISO 8601 format"},
                            "end_time": {"type": "string", "description": "Event end time in ISO 8601 format"},
                            "attendees": {"type": "array", "items": {"type": "string"}, "description": "Optional list of attendee email addresses"}
                        },
                        "required": ["summary", "start_time", "end_time"]
                    }
                }
            ]

            # **Only add `ask_database` if no stored data exists**
            if "last_query_data" not in st.session_state:
                functions.append({
                    "name": "ask_database",
                    "description": "Use this function to answer user questions about data. Output should be a fully formed SQL query.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": f"""
                                            SQL query extracting info to answer the user's question.
                                            SQL should be written using this database schema:
                                            Database type: SQLite
                                            Table: employee_data
                                            Columns: EmpID(Primary Key),FirstName,LastName,StartDate,ExitDate,Title,
                                            Supervisor,ADEmail,BusinessUnit,EmployeeStatus,EmployeeType,PayZone,
                                            EmployeeClassificationType,TerminationType,TerminationDescription,
                                            DepartmentType,Division,DOB,State,JobFunctionDescription,GenderCode,
                                            LocationCode,RaceDesc,MaritalDesc,PerformanceScore,CurrentEmployeeRating
                                            """,
                            }
                        },
                        "required": ["query"],
                    },
                })

            # Call OpenAI to determine the function
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                functions=functions,
                function_call="auto"
            )

            response_message = completion.choices[0].message

            if response_message.function_call:
                function_name = response_message.function_call.name
                args = json.loads(response_message.function_call.arguments)
                logging.info(f"Function call: {function_name} with args: {args}")

                if function_name == "ask_database":
                    handle_database_query(args)
                elif function_name == "visualize_data":
                    handle_visualization(args)
                elif function_name == "create_calendar_event":
                    handle_calendar_event(args)
            else:
                st.session_state.messages.append({"role": "assistant", "content": response_message.content})

            st.session_state.user_input = ""
            # st.rerun()


# Function to handle database queries
def handle_database_query(args):
    query_result = ask_database(args["query"])
    logging.info(f"Query result: {query_result}")
    if isinstance(query_result, pd.DataFrame) and not query_result.empty:
        csv_data = query_result.to_csv(index=False)
        st.dataframe(query_result)  # Default display as a table
        st.session_state.last_query_data = csv_data  # Store data for future visualizations
        st.session_state.last_query_columns = list(query_result.columns)  # Store column names
    else:
        st.session_state.messages.append({"role": "assistant", "content": "No data found for the given query."})

# Function to handle visualization
def handle_visualization(args):
    if "last_query_data" in st.session_state:
        visualize_data(st.session_state.last_query_data, args["chart_type"])
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": "No data available for visualization. Run a query first."}
        )

# Function to handle calendar events
def handle_calendar_event(args):
    logging.info(f"Creating calendar event with args: {args}")

    # Check if last query data is stored in session state
    if "last_query_data" in st.session_state and "FirstName" in st.session_state.last_query_columns and "LastName" in st.session_state.last_query_columns:
        df = pd.read_csv(io.StringIO(st.session_state.last_query_data))

        # Extract FirstName and LastName
        attendees = df.apply(lambda row: f"{row['FirstName']} {row['LastName']}", axis=1).tolist()

        logging.info(f"Using stored employee data for attendees: {attendees}")

        args["attendees"] = attendees  # Assign attendees

        # Proceed with event creation
        result = create_event(
            summary=args.get("summary", "Meeting"),
            start_time_str=args.get("start_time"),
            end_time_str=args.get("end_time"),
            attendees=args["attendees"]
        )

        logging.info(f"Event Created: {result}")
        st.session_state.messages.append({"role": "assistant", "content": f"Meeting successfully scheduled: {result}"})

    else:
        logging.warning("No stored query data found. Requesting attendee names from the user.")
        st.session_state.messages.append({"role": "assistant", "content": "I already have the list of employees, but I need their names to be included for the meeting. Please confirm if I should proceed with the previous results."})



# Main function
def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    initialize_session_state()

    # Hardcoded sidebar with distribution to decorate the application
    with st.sidebar:
        display_employee_status_chart()
        display_employee_type_chart()

    # Main content
    st.title("Calendar and Employee Assistant")
    st.subheader("Chat History")
    render_messages()

    st.subheader("New Message")
    handle_user_input(client)

if __name__ == "__main__":
    main()
