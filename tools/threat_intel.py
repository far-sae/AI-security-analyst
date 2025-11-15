import requests
from typing import Dict, Any, Optional, List
from config import ABUSEIPDB_API_KEY, VIRUSTOTAL_API_KEY, OTX_API_KEY, get_logger

class ThreatIntelClient:
    """
    Simple wrapper to external threat intel APIs.
    Replace endpoints / schemas with real ones or use OpenAPI tools via ADK.
    """

    def __init__(self, trace_id: str = "root"):
        self.logger = get_logger("ThreatIntelClient", trace_id)

    def check_ip(self, ip: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {"ip": ip, "sources": {}, "score": None}

        abuse = self._check_ip_abuseipdb(ip)
        vt = self._check_ip_virustotal(ip)
        otx = self._check_ip_otx(ip)

        result["sources"]["abuseipdb"] = abuse
        result["sources"]["virustotal"] = vt
        result["sources"]["otx"] = otx

        # Very naive scoring
        malicious_counts = sum(
            1 for src in [abuse, vt, otx] if src and src.get("malicious", False)
        )
        result["score"] = malicious_counts / 3 if malicious_counts else 0
        return result

    def _check_ip_abuseipdb(self, ip: str) -> Optional[Dict[str, Any]]:
        if not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY == "SET_ME":
            self.logger.info("Skipping AbuseIPDB check; no API key configured")
            return None

        # Placeholder – replace with real API call.
        try:
            # Example only – not real endpoint
            resp = requests.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers={"Key": ABUSEIPDB_API_KEY},
                params={"ipAddress": ip, "maxAgeInDays": 90},
                timeout=10,
            )
            data = resp.json()
            return {
                "confidence_score": data.get("data", {}).get("abuseConfidenceScore"),
                "malicious": (data.get("data", {}).get("abuseConfidenceScore", 0) > 50),
            }
        except Exception as e:
            self.logger.error(f"AbuseIPDB error: {e}")
            return None

    def _check_ip_virustotal(self, ip: str) -> Optional[Dict[str, Any]]:
        if not VIRUSTOTAL_API_KEY or VIRUSTOTAL_API_KEY == "SET_ME":
            self.logger.info("Skipping VirusTotal check; no API key configured")
            return None
        try:
            # Example only – not real endpoint
            resp = requests.get(
                f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
                headers={"x-apikey": VIRUSTOTAL_API_KEY},
                timeout=10,
            )
            data = resp.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            return {"malicious_count": malicious, "malicious": malicious > 0}
        except Exception as e:
            self.logger.error(f"VirusTotal error: {e}")
            return None

    def _check_ip_otx(self, ip: str) -> Optional[Dict[str, Any]]:
        if not OTX_API_KEY or OTX_API_KEY == "SET_ME":
            self.logger.info("Skipping OTX check; no API key configured")
            return None
        try:
            # Example only – not real endpoint
            resp = requests.get(
                f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
                headers={"X-OTX-API-KEY": OTX_API_KEY},
                timeout=10,
            )
            data = resp.json()
            pulses = data.get("pulse_info", {}).get("count", 0)
            return {"pulse_count": pulses, "malicious": pulses > 0}
        except Exception as e:
            self.logger.error(f"OTX error: {e}")
            return None
