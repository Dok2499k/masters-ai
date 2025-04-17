import os
import json
import requests
from datetime import datetime

TICKETS_DIR = "tickets/"
os.makedirs(TICKETS_DIR, exist_ok=True)

def create_ticket(question: str, username: str = "Unknown User", user_email: str = "user@example.com", custom_title: str = None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ticket_id = f"ticket_{timestamp}"

    title = custom_title if custom_title else f"Question: {question[:50]}..."
    description = f"User: {username}\nEmail: {user_email}\n\nQuestion:\n{question}\n\nCreated at: {datetime.now().isoformat()}"

    # Try creating ticket in Trello
    trello_id = create_trello_card(title, description)

    ticket = {
        "ticket_id": ticket_id,
        "username": username,
        "user_email": user_email,
        "title": title,
        "description": question,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "trello_card_id": trello_id
    }

    ticket_path = os.path.join(TICKETS_DIR, f"{ticket_id}.json")
    with open(ticket_path, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False, indent=4)

    return ticket_id

def create_trello_card(title: str, description: str):
    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")
    list_id = os.getenv("TRELLO_LIST_ID")

    if not all([api_key, api_token, list_id]):
        print("Trello credentials are missing. Skipping Trello card creation.")
        return None

    url = "https://api.trello.com/1/cards"
    query = {
        'key': api_key,
        'token': api_token,
        'idList': list_id,
        'name': title,
        'desc': description
    }

    response = requests.post(url, params=query)
    if response.status_code == 200:
        card = response.json()
        return card['id']
    else:
        print(f"Failed to create Trello card: {response.text}")
        return None
