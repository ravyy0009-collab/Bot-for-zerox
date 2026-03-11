import json
from datetime import datetime

DB_FILE = "database.json"

def load_db():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return {"tickets": {}, "sequence": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def generate_ticket(user_id):
    data = load_db()

    today = datetime.now().strftime("%m%y%d")

    seq = data["sequence"].get(today, 0) + 1
    data["sequence"][today] = seq

    ticket = f"{today}{seq}"

    data["tickets"][ticket] = {
        "user_id": user_id,
        "status": "open"
    }

    save_db(data)

    return ticket

def get_user(ticket):
    data = load_db()
    return data["tickets"].get(ticket, {}).get("user_id")

def resolve_ticket(ticket):
    data = load_db()
    if ticket in data["tickets"]:
        data["tickets"][ticket]["status"] = "resolved"
    save_db(data)