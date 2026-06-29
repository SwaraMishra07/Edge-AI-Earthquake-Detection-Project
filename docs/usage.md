# Usage Guide

## Starting the System

```bash
python -m app.main
```

## Configuration

Create `.env` file with:
```
MQTT_BROKER=localhost
MQTT_PORT=1883
MODEL_PATH=models/earthquake_model.tflite
SENSOR_SAMPLE_RATE=100
DETECTION_THRESHOLD=0.7
```

## API Endpoints

### Get Latest Events
```
GET /api/events
```

### Get Sensor Status
```
GET /api/sensors
```

### Get System Health
```
GET /api/health
```

### Post Manual Alert
```
POST /api/alerts
Content-Type: application/json

{
  "magnitude": 5.2,
  "latitude": 37.5,
  "longitude": -122.3
}
```

## Dashboard

Access the web dashboard at: http://localhost:5000

Features:
- Real-time earthquake detection visualization
- System metrics monitoring
- Alert history
- Sensor status
