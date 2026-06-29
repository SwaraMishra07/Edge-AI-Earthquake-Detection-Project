import numpy as np
from app.alert import should_alert


def test_should_alert_threshold():
    assert should_alert(0.85, 0.8)
    assert not should_alert(0.7, 0.8)
