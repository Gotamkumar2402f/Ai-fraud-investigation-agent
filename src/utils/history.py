import json
import os
from datetime import datetime

HISTORY_FILE = "data/investigation_history.json"

def save_investigation(transaction_id: str, report: str, risk_level: str = "UNKNOWN"):
    """Save investigation result to history."""
    os.makedirs("data", exist_ok=True)
    
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "transaction_id": transaction_id,
        "timestamp": datetime.now().isoformat(),
        "risk_level": risk_level,
        "report": report
    }
    
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    
    history.insert(0, entry)  # newest first
    history = history[:50]    # keep last 50 only
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    return entry["id"]

def get_history():
    """Get all investigation history."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_investigation_by_id(inv_id: str):
    """Get one investigation by id."""
    history = get_history()
    for item in history:
        if item["id"] == inv_id:
            return item
    return None