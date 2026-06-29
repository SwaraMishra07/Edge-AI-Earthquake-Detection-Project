# Edge AI Earthquake Early Alerts

An Edge AI prototype for earthquake early-warning using local inference, peer verification, and a lightweight API.

## Project structure

- `app/` - core edge logic, model inference, MQTT messaging, and API
- `scripts/` - training and deployment helper scripts
- `tests/` - unit tests for preprocessing, inference, and messaging logic
- `docs/` - architecture and usage documentation
- `.github/workflows/` - GitHub Actions CI
- `Dockerfile` - container image for the app

## Tech stack

- Python 3.13
- FastAPI
- SQLite
- MQTT (`paho-mqtt`)
- TensorFlow Lite (`tflite-runtime` or `tensorflow`)
- Docker
- GitHub Actions

## Getting started

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn app.api:app --reload
   ```

## What’s included

- local sensor simulation and preprocessing
- lightweight TFLite inference wrapper
- MQTT publish/subscribe module
- consensus-based alert logic
- small FastAPI dashboard
- GitHub Actions CI

## Notes

The project is scaffolded as a prototype and can be extended with real sensor input, device discovery, and cloud integration.
