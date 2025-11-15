from fastapi import FastAPI, UploadFile, File
from uuid import uuid4

from agents import LogAnalystAgent, ThreatIntelAgent, ResponseAgent, ReportAgent
from config import get_logger

app = FastAPI(title="AI Security Analyst Assistant")


@app.get("/")
async def root():
    return {"message": "AI Security Analyst API is running. Use POST /investigate with a log file."}


@app.post("/investigate")
async def investigate(file: UploadFile = File(...)):
    trace_id = str(uuid4())
    logger = get_logger("API", trace_id)

    # Read uploaded file
    content_bytes = await file.read()
    log_text = content_bytes.decode("utf-8", errors="ignore")
    session_id = trace_id

    logger.info("Starting investigation pipeline")

    # Instantiate agents
    a1 = LogAnalystAgent(trace_id)
    a2 = ThreatIntelAgent(trace_id)
    a3 = ResponseAgent(trace_id)
    a4 = ReportAgent(trace_id)

    # 1) Log analysis (NOW PASS log_text)
    log_result = a1.run(session_id, log_text)

    # 2) Threat intel (async)
    intel_result = await a2.run_async(session_id)

    # 3) Response recommendation (sync Gemini)
    response_result = a3.run(session_id)

    # 4) Report generation (sync)
    report_result = a4.run(session_id)

    return {
        "trace_id": trace_id,
        "log_summary": log_result.get("summary"),
        "threat_intel": intel_result,
        "response_recommendation": response_result,
        "incident_report": report_result.get("incident_report"),
    }
