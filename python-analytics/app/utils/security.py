from datetime import datetime, timedelta, timezone
from ..db import get_alerts_collection

def is_duplicate_alert(rule_name: str, identifier_key: str, identifier_value: str, cooldown_mins: int =10):
    alerts_col = get_alerts_collection()
    now = datetime.now(timezone.utc)
    cooldown_time = now - timedelta(minutes=cooldown_mins)

    # Dynamic query to check for the specific identifier (e.g., source ip)
    query = {
        "rule": rule_name,
        identifier_key: identifier_value,
        "created_at": {"$gte": cooldown_time}
    }

    return alerts_col.find_one(query) is not None

