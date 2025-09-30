# src/vulnerabilities/sqli.py
"""
SQL Injection (basic) checker.
Küçük, eğitim amaçlı; parametre bazlı query tampering yapar ve response içinde known SQL error signature arar.
"""
from typing import List, Optional
import urllib.parse
import logging
from requests import Session, RequestException

from ..models import Finding
from ..core import make_session

LOGGER = logging.getLogger(__name__)

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "pg_query",
    "sql syntax",
    "sqlite error",
]

INJECTION_PAYLOAD = "' OR '1'='1"

def check_sql_injection(url: str, session: Optional[Session] = None) -> List[Finding]:
    """
    Basit parametrik SQLi testi.
    - url içinde query string yoksa [] döner.
    - session verilmemişse make_session ile yeni bir session oluşturulur.
    """
    findings: List[Finding] = []
    session = session or make_session()
    parsed = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if not qs:
        LOGGER.debug("check_sql_injection: URL'de query parametresi yok: %s", url)
        return findings

    # Her parametrenin ilk değerine payload ekle
    tampered = {k: [v[0] + INJECTION_PAYLOAD] for k, v in qs.items()}
    new_qs = urllib.parse.urlencode(tampered, doseq=True)
    test_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, new_qs, parsed.fragment)
    )
    LOGGER.info("check_sql_injection: testing %s", test_url)

    try:
        r = session.get(test_url, timeout=getattr(session, "request_timeout", 10))
        text = r.text.lower()
        for sig in SQL_ERRORS:
            if sig in text:
                findings.append(
                    Finding(
                        type="SQLi",
                        detail=f"Sorgu parametresi: {list(qs.keys())}",
                        evidence=f"İmza: {sig}",
                        severity="high",
                    )
                )
                LOGGER.warning("SQLi signature found (%s) at %s", sig, test_url)
                break
    except RequestException as e:
        LOGGER.error("Network error during SQLi check: %s", e)
        findings.append(Finding(type="Network", detail="SQLi isteği başarısız", evidence=str(e), severity="low"))

    return findings
