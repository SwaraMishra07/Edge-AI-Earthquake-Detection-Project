from app.sensor import simulate_sensor_data
from app.preprocessing import normalize_signal, extract_features
from app.inference import load_model, run_inference
from app.alert import build_alert, should_alert
from app.config import SAMPLE_RATE, WINDOW_SIZE, ALERT_THRESHOLD


def main() -> None:
    samples = simulate_sensor_data(SAMPLE_RATE, duration_seconds=2.0)
    normalized = normalize_signal(samples)
    features = extract_features(normalized)

    try:
        interpreter = load_model()
        score = run_inference(interpreter, features)
    except FileNotFoundError:
        score = 0.0

    alert_needed = should_alert(score, ALERT_THRESHOLD)
    payload = build_alert(
        event_id="demo-0001",
        confidence=score,
        message="Earthquake-like event detected" if alert_needed else "No significant event detected",
    )
    print(payload)


if __name__ == "__main__":
    main()
