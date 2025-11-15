from typing import Dict, Any
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, get_logger, session_state

class ResponseAgent:
    """
    Agent 3: uses Gemini to suggest actions, map to MITRE, and prioritize alerts.
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("ResponseAgent", trace_id)
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
            genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def run(self, session_id: str) -> Dict[str, Any]:
        suspicious_logs = session_state.get_memory(session_id, "suspicious_logs", [])
        threat_intel = session_state.get_memory(session_id, "threat_intel", {})

        prompt = f"""
You are a senior SOC analyst.

You are given:
1. Suspicious log records (JSON):
{suspicious_logs}

2. Threat intelligence lookups for IPs:
{threat_intel}

Tasks:
- Identify likely attack type(s).
- Map to MITRE ATT&CK techniques.
- Prioritize severity (Low/Medium/High/Critical).
- Suggest concrete remediation actions an analyst should take.
- Highlight any indicators of compromise (IOCs).

Return your answer as structured JSON with keys:
"attack_summary", "mitre_techniques", "severity", "remediation_steps", "ioc_list".
"""

        self.logger.info("Calling Gemini for response recommendation")

        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            self.logger.warning("No real Gemini API key configured, returning mock response")
            result = {
                "attack_summary": "Brute force SSH login attempts from suspicious IPs.",
                "mitre_techniques": ["T1110 - Brute Force"],
                "severity": "High",
                "remediation_steps": [
                    "Block offending IPs at firewall.",
                    "Enable rate limiting for SSH.",
                    "Enforce key-based auth only.",
                ],
                "ioc_list": list(threat_intel.keys()),
            }
        else:
            response = self.model.generate_content(prompt)
            # Try to parse as JSON, or fallback to text
            try:
                import json
                result = json.loads(response.text)
            except Exception:
                result = {"raw_response": response.text}

        session_state.add_memory(session_id, "response_recommendation", result)
        return result
