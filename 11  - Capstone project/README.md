# Calendar Assistant

This is a Python-based Calendar Assistant that integrates with Google Calendar and OpenAI to help users create and fetch calendar events through a Streamlit-based interface.

---

## Features

- Create Google Calendar events.
- Fetch events for specific periods from Google Calendar.
- Interactive chat interface powered by OpenAI.
- Logs all activities to the console for debugging.

---

## Prerequisites

1. **Python**: Ensure Python 3.8 or later is installed on your system.
2. **Google Cloud Project**: Set up a Google Cloud project and enable the Google Calendar API.
   - Download `credentials.json` from your Google Cloud project.
   - Place the `credentials.json` file in the root directory of this project.
3. **OpenAI API Key**: Obtain your OpenAI API key from [OpenAI](https://platform.openai.com/).
   - Add your API key to a `.env` file in the root directory:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

---

## Installation Instructions

Follow these steps to set up and run the project:

### 1. Clone the Repository
```
git clone https://github.com/Dok2499k/masters-ai.git
cd 11\ \ -\ Capstone\ project/
```

### 2. Create and Activate a Virtual Environment
```
python3 -m venv venv

# On Mac and Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Required Packages
Install the necessary dependencies using pip:
```
pip install -r requirements.txt
```

### 4. Add Google Credentials
- Place the `credentials.json` file in the project root directory.
- Ensure you have write access to save the `token.json` file generated during authentication.

### 5. Set Up the `.env` File
Create a `.env` file in the root directory and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_openai_api_key
```

### 6. Run the Application
Launch the Streamlit app:
```
streamlit run streamlit_app.py
```

### 7. Authenticate with Google Calendar
- On first run, you will be prompted to authenticate with your Google account.
- This will generate a `token.json` file for future use.

---

## Usage

1. Open the Streamlit application in your web browser (default URL: `http://localhost:8501`).
2. Use the chat interface to:
   - Schedule new calendar events.
   - Retrieve events for specific date ranges.

---

## Logging

All actions are logged to the console for debugging. Logs include:
- API requests and responses.
- User interactions.
- Errors and exceptions.

---

## Troubleshooting

1. **Invalid API Key**: Ensure your OpenAI API key is valid and correctly set in the `.env` file.
2. **Google Calendar API Errors**:
   - Check that the `credentials.json` file is valid and has the necessary permissions.
   - Ensure the `token.json` file is generated correctly after authentication.
3. **Python Version Issues**: Use Python 3.8 or later.