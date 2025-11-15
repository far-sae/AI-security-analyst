import json
from pathlib import Path
from uuid import uuid4

from agents import LogAnalystAgent, ThreatIntelAgent, ResponseAgent, ReportAgent
from evaluation.evaluator import SimpleEvaluator
from config import get_logger


def load_all_samples():
    """
    Loads all JSON files inside sample_data/ and returns a dict:
    {
        "filename.json": "<raw log text>",
        ...
    }
    """
    folder = Path("sample_data")
    files = list(folder.glob("*.json"))

    samples = {}
    for f in files:
        try:
            samples[f.name] = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Could not read {f}: {e}")

    return samples


def run_pipeline_on_log(logs_text: str, trace_id: str):
    """
    Runs the full agent pipeline on a single log file.
    """
    session_id = trace_id

    a1 = LogAnalystAgent(trace_id)
    a2 = ThreatIntelAgent(trace_id)
    a3 = ResponseAgent(trace_id)
    a4 = ReportAgent(trace_id)

    # 1) Log Analysis
    log_result = a1.run(session_id, logs_text)

    # 2) Threat Intel
    intel_result = a2.run(session_id)   # sync version OK in CLI

    # 3) Response Recommendation
    response_result = a3.run(session_id)

    # 4) Incident Report
    report_result = a4.run(session_id)

    # 5) Evaluation
    evaluator = SimpleEvaluator(trace_id)
    eval_result = evaluator.evaluate_report(report_result)

    return {
        "log_summary": log_result["summary"],
        "intel": intel_result,
        "response": response_result,
        "report": report_result,
        "evaluation": eval_result
    }


def main():
    logger = get_logger("Main", "CLI")
    logger.info("Starting AI Security Analyst Assistant - Batch Mode")

    # Load all sample logs
    samples = load_all_samples()

    if not samples:
        print("No log files found in sample_data/")
        return

    print(f"Found {len(samples)} sample log files.\n")

    # Run pipeline for each log file
    for filename, logs_text in samples.items():
        trace_id = str(uuid4())
        print("\n" + "=" * 80)
        print(f"📝 Processing: {filename}")
        print("=" * 80)

        results = run_pipeline_on_log(logs_text, trace_id)

        print("\n=== LOG SUMMARY ===")
        print(results["log_summary"])

        print("\n=== THREAT INTEL (per IP) ===")
        print(json.dumps(results["intel"], indent=2))

        print("\n=== RESPONSE RECOMMENDATION ===")
        print(json.dumps(results["response"], indent=2))

        print("\n=== INCIDENT REPORT ===")
        print(results["report"]["incident_report"])

        print("\n=== EVALUATION ===")
        print(json.dumps(results["evaluation"], indent=2))

        print("\nFinished Processing:", filename)


if __name__ == "__main__":
    main()
