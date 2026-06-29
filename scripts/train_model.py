import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import joblib

MODEL_DIR = Path(__file__).resolve().parent.parent / "app" / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def build_dataset(samples: int = 200):
    X = []
    y = []
    for _ in range(samples):
        noise = np.random.normal(0, 0.02, size=(200, 3))
        features = np.hstack([
            np.mean(noise, axis=0),
            np.std(noise, axis=0),
            np.max(noise, axis=0),
            np.min(noise, axis=0),
        ])
        X.append(features)
        y.append(0)

    for _ in range(samples):
        event = np.random.normal(0, 0.02, size=(200, 3))
        event[90:110, 0] += np.linspace(0, 2.0, 20)
        features = np.hstack([
            np.mean(event, axis=0),
            np.std(event, axis=0),
            np.max(event, axis=0),
            np.min(event, axis=0),
        ])
        X.append(features)
        y.append(1)

    return np.array(X), np.array(y)


def main():
    X, y = build_dataset()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clf = LogisticRegression(max_iter=500)
    clf.fit(X_scaled, y)

    joblib.dump(clf, MODEL_DIR / "demo_model.joblib")
    joblib.dump(scaler, MODEL_DIR / "demo_scaler.joblib")
    print("Saved demo_model.joblib and demo_scaler.joblib")


if __name__ == "__main__":
    main()
