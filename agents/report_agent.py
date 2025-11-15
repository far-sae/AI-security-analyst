from typing import Dict, Any
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, get_logger, session_state

class ReportAgent:
    """
    Agent 4: loop agent that refines the final incident report.
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("ReportAgent", trace_id)
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
            genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def run(self, session_id: str, max_iterations: int = 3) -> Dict[str, Any]:
        parsed_logs = session_state.get_memory(session_id, "parsed_logs", [])
        suspicious_logs = session_state.get_memory(session_id, "suspicious_logs", [])
        threat_intel = session_state.get_memory(session_id, "threat_intel", {})
        response_rec = session_state.get_memory(session_id, "response_recommendation", {})

        base_prompt = f"""
You are an experienced SOC incident responder.

Create a professional incident report with:

- Executive Summary
- Timeline of Events
- Indicators of Compromise (IOCs)
- Attack Narrative (what likely happened)
- MITRE ATT&CK mapping
- Severity
- Detailed Technical Findings
- Recommended Remediation Actions
- Next Steps

Data you can use:

1) Parsed logs:
{parsed_logs}

2) Suspicious logs:
{suspicious_logs}

3) Threat intelligence:
{threat_intel}

4) Response recommendation:
{response_rec}
"""

        draft = None
        for i in range(max_iterations):
            self.logger.info(f"Report refinement iteration {i+1}/{max_iterations}")

            if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
                # Mock behaviour
                draft = "Incident Report (mock)\n\n" \
                        "Executive Summary: Brute force attempts detected.\n" \
                        "Severity: High\n" \
                        "Remediation: Block IPs, enforce MFA."
                break
            else:
                prompt = base_prompt
                if draft:
                    prompt += f"\n\nHere is the previous draft. Improve clarity and structure:\n\n{draft}"

                response = self.model.generate_content(prompt)
                draft = response.text  # free-form text is fine

        report = {
            "incident_report": draft,
            "iterations": min(max_iterations, 1 if not GEMINI_API_KEY else max_iterations),
        }
        session_state.add_memory(session_id, "incident_report", report)
        return report
