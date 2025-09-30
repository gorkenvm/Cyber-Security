# src/vulnerabilities/ports.py
"""
Basit TCP port tarama ve banner okuma (kısa timeout ile).
Eğitim amaçlıdır: yüksek hızda veya büyük port listelerinde daha iyi çözümler (nmap, async) gerekir.
"""
from typing import List
import socket
import logging

from ..models import Finding

LOGGER = logging.getLogger(__name__)

def check_open_ports(host: str, ports: List[int], timeout: float = 1.0) -> List[Finding]:
    """
    host: hostname veya IP
    ports: int list
    timeout: bağlantı ve recv timeout (saniye)
    """
    findings: List[Finding] = []
    for p in ports:
        try:
            LOGGER.debug("Checking %s:%d", host, p)
            with socket.create_connection((host, p), timeout=timeout) as s:
                s.settimeout(timeout)
                banner = ""
                try:
                    banner = s.recv(256).decode(errors="ignore").strip()
                except socket.timeout:
                    # banner alınamadı ama port açık olabilir
                    banner = ""
                findings.append(
                    Finding(
                        type="Open-Port",
                        detail=f"{host}:{p}",
                        evidence=banner or "banner yok",
                        severity="low",
                    )
                )
                LOGGER.info("Open port found: %s:%d (banner: %s)", host, p, banner or "<empty>")
        except OSError:
            # kapalı / unreachable -> skip
            LOGGER.debug("Port closed or unreachable: %s:%d", host, p)
            continue
    return findings
