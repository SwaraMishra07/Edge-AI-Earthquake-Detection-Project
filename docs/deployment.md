# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- TensorFlow 2.x
- MQTT Broker (Mosquitto)

## Local Development

```bash
docker-compose up -d
python -m app.main
```

## Production Deployment

### Using Docker

```bash
docker build -t earthquake-detector .
docker run -d \
  -e MQTT_BROKER=mqtt_broker \
  -e MODEL_PATH=/app/models/earthquake_model.tflite \
  earthquake-detector
```

### Using Kubernetes

See deployment manifests in `deployment/` directory.

## Configuration

Set environment variables in `.env`:
- `MQTT_BROKER`: MQTT broker hostname
- `MQTT_PORT`: MQTT broker port
- `MODEL_PATH`: Path to TFLite model
- `SENSITIVITY`: Detection sensitivity threshold

## Monitoring

Access monitoring dashboards:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
