import json
from typing import List, Dict, Any

def parse_logs(log_content: str) -> List[Dict[str, Any]]:
    """
    Very simple JSON-lines / JSON array log parser.
    You can extend this for CSV, syslog, Windows logs etc.

    Returns a list of records with simple anomaly tags.
    """
    records: List[Dict[str, Any]] = []

    try:
        # Try JSON array
        data = json.loads(log_content)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError:
        # Try JSONL
        data = []
        for line in log_content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    for rec in data:
        rec = rec.copy()
        # Extremely naive "anomaly" tagging for demo
        message = str(rec.get("message", "")).lower()
        tags = []

        if "failed password" in message or "authentication failure" in message:
            tags.append("auth_failure")
        if "sudo" in message and "not in sudoers" in message:
            tags.append("privilege_escalation_attempt")
        if "connection from" in message and "blacklisted" in message:
            tags.append("connection_from_blacklisted_ip")

        rec["tags"] = tags
        records.append(rec)

    return records
