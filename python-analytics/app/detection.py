from datetime import datetime, timedelta, timezone
from .db import get_logs_collection, get_alerts_collection
from .utils.security import is_duplicate_alert
from .rules_config import DETECTION_RULES

from datetime import datetime, timezone, timedelta
from .db import get_logs_collection, get_alerts_collection
from .utils.security import is_duplicate_alert
from .rules_config import DETECTION_RULES

def run_all_detections():
    """Iterates through all rules defined in config and executes them."""
    alerts_col = get_alerts_collection()
    now = datetime.now(timezone.utc)

    for rule in DETECTION_RULES:
        logs_col = get_logs_collection()
        
        # Inject the time window into the first stage of the pipeline
        time_filter = {"timestamp": {"$gte": now - timedelta(minutes=rule["window_mins"])}}
        
        # Prepare the pipeline by adding the time filter to the start
        pipeline = [{"$match": time_filter}] + rule["pipeline"]

        results = list(logs_col.aggregate(pipeline))

        for r in results:
            identifier_value = r["_id"]

            # Use our centralized deduplication
            if is_duplicate_alert(rule["name"], rule["identifier_field"], identifier_value, rule["cooldown_mins"]):
                continue

            alert = {
                "rule": rule["name"],
                rule["identifier_field"]: identifier_value,
                "count": r.get("count", 1),
                "severity": rule["severity"],
                "created_at": now
            }
            alerts_col.insert_one(alert)
            print(f"[{rule['severity'].upper()}] Alert generated: {rule['name']} for {identifier_value}", flush=True)

   
