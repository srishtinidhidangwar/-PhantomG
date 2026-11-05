"""Hand-crafted feature engineering for PhantomG.

Each feature targets a common phishing tactic: urgency, reward bait, suspicious
links, threats, requests for sensitive data, and impersonal greetings.
"""
import re
from typing import Dict, List

URGENCY = ["urgent", "immediately", "act now", "right away", "asap", "within 24 hours",
           "expires", "last chance", "final notice", "limited time", "verify now", "as soon as possible"]
PRIZE = ["congratulations", "winner", "you have won", "prize", "reward", "free gift",
         "lottery", "claim your", "cash", "bonus", "gift card", "selected"]
THREAT = ["suspended", "terminated", "locked", "unauthorized", "unusual activity", "legal action",
          "will be closed", "deactivated", "penalty", "account will be", "security alert", "compromised"]
SENSITIVE = ["password", "pin", "otp", "ssn", "social security", "credit card", "card number",
             "cvv", "bank account", "login", "credentials", "verify your account", "confirm your identity"]
GENERIC_GREETING = ["dear user", "dear customer", "dear member", "dear account holder",
                    "dear sir", "dear madam", "valued customer", "dear client"]

URL_RE = re.compile(r"(https?://[^\s]+|www\.[^\s]+)", re.IGNORECASE)
IP_URL_RE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}")
SHORTENER_RE = re.compile(r"(bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|cutt\.ly)", re.IGNORECASE)
SUSPICIOUS_TLD_RE = re.compile(r"\.(xyz|top|click|tk|ml|ga|cf|gq|work|info)(/|\s|$)", re.IGNORECASE)

FEATURE_NAMES: List[str] = [
    "urgency_count", "prize_count", "threat_count", "sensitive_count", "generic_greeting",
    "url_count", "ip_url", "shortener_url", "suspicious_tld", "exclamation_count",
    "uppercase_ratio", "text_length", "digit_ratio",
]

# Human-readable labels shown in the GUI / CLI for each triggered feature.
INDICATOR_LABELS = {
    "urgency_count": "Urgency language detected",
    "prize_count": "Prize / reward bait language",
    "threat_count": "Threat or consequence phrases",
    "sensitive_count": "Requests for sensitive information",
    "generic_greeting": "Generic greeting (no personal name)",
    "url_count": "Contains links",
    "ip_url": "Link points to a raw IP address",
    "shortener_url": "Shortened URL hides destination",
    "suspicious_tld": "Link uses a suspicious domain ending",
    "exclamation_count": "Excessive exclamation marks",
}


def _count(text: str, phrases: List[str]) -> int:
    return sum(text.count(p) for p in phrases)


def extract_features(text: str) -> Dict[str, float]:
    """Return a dict of numeric features for a single email body."""
    text = text or ""
    low = text.lower()
    n = max(len(text), 1)
    return {
        "urgency_count": _count(low, URGENCY),
        "prize_count": _count(low, PRIZE),
        "threat_count": _count(low, THREAT),
        "sensitive_count": _count(low, SENSITIVE),
        "generic_greeting": int(any(g in low for g in GENERIC_GREETING)),
        "url_count": len(URL_RE.findall(text)),
        "ip_url": int(bool(IP_URL_RE.search(text))),
        "shortener_url": int(bool(SHORTENER_RE.search(text))),
        "suspicious_tld": int(bool(SUSPICIOUS_TLD_RE.search(text))),
        "exclamation_count": text.count("!"),
        "uppercase_ratio": sum(c.isupper() for c in text) / n,
        "text_length": len(text),
        "digit_ratio": sum(c.isdigit() for c in text) / n,
    }


def feature_vector(text: str) -> List[float]:
    f = extract_features(text)
    return [f[name] for name in FEATURE_NAMES]


def threat_indicators(text: str) -> List[str]:
    """List the human-readable indicators triggered by this email."""
    f = extract_features(text)
    out = []
    for key, label in INDICATOR_LABELS.items():
        if key == "exclamation_count":
            if f[key] >= 3:
                out.append(label)
        elif f[key] > 0:
            out.append(label)
    return out
