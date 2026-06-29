from collections import deque
from app.consensus import needs_alert


def test_needs_alert_false_without_threshold():
    assert not needs_alert(0.5, deque([0.9, 0.95]), 0.8, 2)


def test_needs_alert_true_with_peer_count():
    assert needs_alert(0.9, deque([0.85, 0.9]), 0.8, 2)
