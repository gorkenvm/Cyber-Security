# src/models.py
from dataclasses import dataclass

@dataclass
class Finding:
    """
    Basit bulgu modeli.
    - type: vulnerability type short key (e.g., "SQLi", "XSS-Reflected", "Open-Port")
    - detail: detaylı açıklama / hedef
    - evidence: kanıt / snippet
    - severity: 'low'|'medium'|'high'
    """
    type: str
    detail: str
    evidence: str
    severity: str = "medium"
