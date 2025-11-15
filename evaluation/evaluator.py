from typing import Dict, Any, List
from config import get_logger

class SimpleEvaluator:
    """
    Very lightweight evaluator for the agent output.
    Not a strict metric – more like a rubric to show evaluability.
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("SimpleEvaluator", trace_id)

    def evaluate_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        text = report.get("incident_report", "") or ""
        score = 0
        criteria = {}

        def has(section: str, key: str):
            nonlocal score
            if section.lower() in text.lower():
                score += 1
                criteria[key] = True
            else:
                criteria[key] = False

        has("executive summary", "has_executive_summary")
        has("timeline", "has_timeline")
        has("indicators of compromise", "has_iocs")
        has("remediation", "has_remediation")

        return {
            "score": score,
            "criteria": criteria,
        }
