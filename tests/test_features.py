import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features import FEATURE_NAMES, extract_features, feature_vector, threat_indicators

PHISH = "Dear User, URGENT: verify your password immediately at http://192.168.1.5/login or your account will be suspended!!!"
SAFE = "Hi Sam, the meeting is at 3 PM tomorrow. See you then."


def test_vector_length_matches_names():
    assert len(feature_vector(PHISH)) == len(FEATURE_NAMES)


def test_phish_triggers_features():
    f = extract_features(PHISH)
    assert f["urgency_count"] > 0 and f["sensitive_count"] > 0
    assert f["generic_greeting"] == 1 and f["ip_url"] == 1 and f["url_count"] == 1


def test_safe_is_clean():
    assert threat_indicators(SAFE) == []


def test_empty_input():
    assert extract_features("")["url_count"] == 0
