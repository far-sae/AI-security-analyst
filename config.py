import os
from dotenv import load_dotenv
import logging
from collections import defaultdict
from typing import Dict, Any

load_dotenv()

# ---- LLM / Gemini config ----
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")  # DO NOT COMMIT REAL KEYS

# ---- Threat intel APIs (placeholders) ----
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "SET_ME")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "SET_ME")
OTX_API_KEY = os.getenv("OTX_API_KEY", "SET_ME")

# ---- Logging / Observability ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [trace_id=%(trace_id)s] %(message)s",
)

# Small wrapper to attach a trace_id
class TraceLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        if "extra" in kwargs:
            extra.update(kwargs["extra"])
        kwargs["extra"] = extra
        return msg, kwargs

def get_logger(name: str, trace_id: str = "root") -> TraceLoggerAdapter:
    logger = logging.getLogger(name)
    return TraceLoggerAdapter(logger, {"trace_id": trace_id})

# ---- Simple Session + Memory ----
class SessionState:
    """
    Very simple in-memory session and memory.
    In a real system you'd plug into ADK's InMemorySessionService or similar.
    """
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = defaultdict(dict)

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self.sessions[session_id]

    def add_memory(self, session_id: str, key: str, value: Any):
        self.sessions[session_id].setdefault("memory", {})
        self.sessions[session_id]["memory"][key] = value

    def get_memory(self, session_id: str, key: str, default=None):
        return self.sessions[session_id].get("memory", {}).get(key, default)

session_state = SessionState()
