import numpy as np
from app.preprocessing import normalize_signal, extract_features


def test_normalize_signal_returns_zero_mean():
    sample = np.array([[1.0, 0.0, -1.0], [3.0, 0.0, -3.0]])
    normalized = normalize_signal(sample)
    assert np.allclose(np.mean(normalized, axis=0), 0.0)


def test_extract_features_shape():
    window = np.ones((100, 3))
    features = extract_features(window)
    assert features.shape == (12,)
