# src/core.py
"""
Temel HTTP session üreticisi, retry ve basit timeout desteği sağlar.
Vulnerabilities modülleri make_session() ile session alır.
"""

from typing import Optional
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

LOGGER = logging.getLogger(__name__)

def make_session(retries: int = 2, backoff: float = 0.3, timeout: int = 10) -> requests.Session:
    """
    requests.Session döndürür; retry ve user-agent ayarlanır.
    session.request_timeout ile timeout değerini saklarız (kolay erişim için).
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": "mini-scanner/0.1 (+https://github.com/yourname/mini-scanner)"
    })

    # Retry policy: belirli HTTP statuslarında retry yap
    retry = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)

    # convenience attribute
    s.request_timeout = timeout
    LOGGER.debug("make_session created with timeout=%s retries=%s", timeout, retries)
    return s
