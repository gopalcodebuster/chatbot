import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "db.json"

def read_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def find_faq(query: str):
    db = read_db()
    q = query.lower()
    matches = [
        f for f in db["faqs"]
        if q in f["question"].lower() or q in f["answer"].lower()
    ]
    return matches
