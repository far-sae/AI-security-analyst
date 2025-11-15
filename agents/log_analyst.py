from typing import Dict, Any, List
from tools import parse_logs
from config import get_logger, session_state

class LogAnalystAgent:
    """
    Agent 1: parses logs and extracts suspicious events.
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("LogAnalystAgent", trace_id)

    def run(self, session_id: str, raw_logs: str) -> Dict[str, Any]:
        self.logger.info("Starting log analysis")
        parsed = parse_logs(raw_logs)

        suspicious = [rec for rec in parsed if rec.get("tags")]
        self.logger.info(f"Found {len(suspicious)} suspicious records")

        # Save to session memory
        session_state.add_memory(session_id, "parsed_logs", parsed)
        session_state.add_memory(session_id, "suspicious_logs", suspicious)

        return {
            "parsed_logs": parsed,
            "suspicious_logs": suspicious,
            "summary": f"Parsed {len(parsed)} records; found {len(suspicious)} suspicious events.",
        }
