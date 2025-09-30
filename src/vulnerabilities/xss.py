# src/vulnerabilities/xss.py
"""
Reflected XSS checker (basic).
Payload'ı parametrelerle gönderir, sayfa çıktısında payload veya encode edilmiş halleri kontrol eder.
"""
from typing import List, Optional
import urllib.parse
import logging
from bs4 import BeautifulSoup
from requests import Session, RequestException

from ..models import Finding
from ..core import make_session

LOGGER = logging.getLogger(__name__)

XSS_PAYLOAD = "<svg/onload=alert(1)>"

def check_xss_reflected(url: str, session: Optional[Session] = None) -> List[Finding]:
    """
    Basit yansıyan XSS testi.
    - url'de param yoksa 'q' adında bir param ekler.
    """
    findings: List[Finding] = []
    session = session or make_session()
    parsed = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if not qs:
        qs = {"q": ["test"]}

    tampered = {k: [XSS_PAYLOAD] for k in qs.keys()}
    new_qs = urllib.parse.urlencode(tampered, doseq=True)
    test_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, new_qs, parsed.fragment)
    )
    LOGGER.info("check_xss_reflected: testing %s", test_url)

    try:
        r = session.get(test_url, timeout=getattr(session, "request_timeout", 10))
        body = r.text
        # Direkt payload var mı?
        if XSS_PAYLOAD in body:
            findings.append(
                Finding(
                    type="XSS-Reflected",
                    detail=f"Parametreler: {list(qs.keys())}",
                    evidence="Payload ham olarak çıktı içinde bulundu",
                    severity="high",
                )
            )
            LOGGER.warning("Reflected XSS (raw) detected at %s", test_url)
            return findings

        # HTML encode edilmiş / escaped olabilir: text olarak çıkar mı?
        soup = BeautifulSoup(body, "html.parser")
        if XSS_PAYLOAD in soup.get_text():
            findings.append(
                Finding(
                    type="XSS-Reflected",
                    detail=f"Parametreler: {list(qs.keys())}",
                    evidence="Payload metin olarak (muhtemelen encoded) göründü",
                    severity="medium",
                )
            )
            LOGGER.warning("Reflected XSS (encoded) possible at %s", test_url)
    except RequestException as e:
        LOGGER.error("Network error during XSS check: %s", e)
        findings.append(Finding(type="Network", detail="XSS isteği başarısız", evidence=str(e), severity="low"))

    return findings
