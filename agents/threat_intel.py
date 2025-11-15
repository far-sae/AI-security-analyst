import asyncio
from typing import Dict, Any
from tools import ThreatIntelClient
from config import get_logger, session_state


class ThreatIntelAgent:
    """
    Agent 2: runs parallel threat intel lookups.

    - Use .run_async(...) inside async code (FastAPI)
    - Use .run(...) inside sync code (CLI main.py)
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("ThreatIntelAgent", trace_id)
        self.client = ThreatIntelClient(trace_id)

    async def _lookup_ip(self, ip: str) -> Dict[str, Any]:
        """
        Wrapper to make the (sync) client check look async-friendly.
        In a real-world case you might use an async HTTP client instead.
        """
        self.logger.info(f"Checking IP {ip}")
        # This runs synchronously; for demo it's fine.
        return self.client.check_ip(ip)

    async def run_async(self, session_id: str) -> Dict[str, Any]:
        """
        Async version: use this inside FastAPI or any async context.
        """
        suspicious_logs = session_state.get_memory(session_id, "suspicious_logs", [])
        ips = set()

        for rec in suspicious_logs:
            ip = rec.get("src_ip") or rec.get("ip") or rec.get("source_ip")
            if ip:
                ips.add(ip)

        self.logger.info(f"Running threat intel for {len(ips)} IPs")

        if not ips:
            intel_by_ip: Dict[str, Any] = {}
        else:
            results = await asyncio.gather(
                *(self._lookup_ip(ip) for ip in ips),
                return_exceptions=False,
            )
            intel_by_ip = {ip: res for ip, res in zip(ips, results)}

        session_state.add_memory(session_id, "threat_intel", intel_by_ip)

        return {
            "ips": list(ips),
            "results": intel_by_ip,
        }

    def run(self, session_id: str) -> Dict[str, Any]:
        """
        Sync wrapper: safe to call from main.py (CLI).

        DO NOT use this inside FastAPI or any existing event loop.
        """
        return asyncio.run(self.run_async(session_id))
