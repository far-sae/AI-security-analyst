AI Security Analyst Assistant
A multi-agent cybersecurity system powered by Google Gemini that automates log analysis, anomaly detection, threat intelligence, incident response, and report generation. Designed for SOC analysts and security engineers, this project demonstrates advanced agent orchestration, async operations, memory, and real-world automation workflows.
🚀 Overview
The AI Security Analyst Assistant is an enterprise-grade multi-agent system that processes security logs and produces:
🔍 Automated Log Analysis
🛡 Parallel Threat Intelligence Lookups
⚠️ Suspicious Activity Detection
📊 Incident Summary & MITRE Mapping
📝 Full Incident Report (LLM-generated & refined)
🤖 Agent-to-Agent Evaluation
🌐 FastAPI Deployment + CLI Batch Mode
Built as part of the Google GenAI Agents Intensive Capstone Project, this system demonstrates effective use of agent architectures, tools, memory, observability, and LLM-driven reasoning.
🧠 System Architecture
User Input (Log File / CLI)
         |
         ▼
┌────────────────────┐
│ Log Analyst Agent   │
└────────────────────┘
         |
         ▼
┌────────────────────┐
│ Threat Intel Agent  │  (Async / Parallel)
└────────────────────┘
         |
         ▼
┌────────────────────┐
│ Response Agent      │ (Gemini)
└────────────────────┘
         |
         ▼
┌────────────────────┐
│ Report Agent        │ (Refinement Loop)
└────────────────────┘
         |
         ▼
┌────────────────────┐
│ Evaluator Agent     │
└────────────────────┘
         |
         ▼
 Final Incident Report JSON
🛠 Key Features
✔ Multi-Agent Workflow
Dedicated agents for logs, intel, response, reporting, evaluation
Sequential + parallel agent execution
Loop-based report refinement
✔ Advanced Tooling
Custom threat-intel lookup tool
Log parsing and anomaly tagging
Shared session memory across agents
✔ Gemini Integration
Gemini Pro used for:
Response generation
Report generation
Evaluation logic
✔ Async + FastAPI Deployment
/investigate endpoint for log uploads
Fully async-safe threat intel workflows
Clean JSON outputs
✔ Batch CLI Mode
Run all logs inside sample_data/ with:
python main.py
📁 Project Structure
├── agents/
│   ├── log_analyst.py
│   ├── threat_intel.py
│   ├── response_agent.py
│   ├── report_agent.py
│   └── __init__.py
├── tools/
│   ├── parser.py
│   ├── threat_intel_client.py
│   └── __init__.py
├── deployment/
│   ├── app.py                # FastAPI server
│   └── Dockerfile
├── evaluation/
│   └── evaluator.py
├── sample_data/
│   ├── ddos_attack_logs.json
│   ├── phishing_logs.json
│   ├── ransomware_logs.json
│   └── ...
├── main.py                   # CLI batch runner
├── config.py
├── requirements.txt
└── README.md
🧪 How to Run (Local)
1. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
2. Install Dependencies
pip install -r requirements.txt
3. Set Gemini API Key
export GEMINI_API_KEY="your_key_here"
4. Start the API
uvicorn deployment.app:app --reload
Open Swagger Docs:
👉 http://127.0.0.1:8000/docs
5. Run Batch CLI Mode
python main.py
📊 Example Output
Log summary
Detected IOC patterns
Threat intel results
Recommended actions
Full AI-generated incident report
Evaluation score
📦 Sample Logs Included
The project includes high-quality sample datasets:
DDoS attack logs
Phishing email headers
Ransomware encryption logs
Kubernetes security logs
Active Directory event logs
VPN brute-force logs
Zero-day exploit payload attempts
Drop your own logs into sample_data/ and run the system instantly.
🏛 Built For
Google GenAI Agents Intensive Capstone Project
Enterprise cybersecurity teams
SOC automation research
AI-driven incident response
Advanced agent architecture learning

