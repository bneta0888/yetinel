from datetime import timedelta

# Define all your detection rules here
DETECTION_RULES = [
    {
        "name": "Multiple Failed Logins",
        "collection": "logs",
        "window_mins": 2,
        "cooldown_mins": 10,
        "identifier_field": "source_ip",
        "severity": "medium",
        "pipeline": [
            {"$match": {"event": "login_failed"}},
            {
                "$group": {
                    "_id": {
                        "ip": "$source_ip",
                        "agent": "$agent_id" # Group by both!
                    },
                    "count": {"$sum": 1}
                }
            },
        {"$match": {"count": {"$gte": 5}}}
        ]
    },
    {
        "name": "Admin Level Activity",
        "collection": "logs",
        "window_mins": 5,
        "cooldown_mins": 30,
        "identifier_field": "source_ip",
        "severity": "high",
        "pipeline": [
            {"$match": {"level": "critical", "event": "admin_login"}},
            {"$group": {"_id": "$source_ip", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gte": 1}}}
        ]
    }
]
