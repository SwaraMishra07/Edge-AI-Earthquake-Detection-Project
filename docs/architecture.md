# System Architecture

## Overview

The Edge AI Earthquake Detection System is designed to detect earthquakes in real-time using edge computing and machine learning.

## Components

### Core Components
- **Sensor**: Collects seismic data from accelerometers
- **Preprocessing**: Normalizes and prepares data for inference
- **Inference**: Runs ML model to detect earthquake patterns
- **Consensus**: Aggregates predictions from multiple sensors
- **Alert System**: Generates and distributes alerts
- **Storage**: Persists event data

### Support Components
- **MQTT Client**: Communicates with edge devices
- **API**: Provides RESTful interface
- **Dashboard**: Web-based monitoring interface

## Data Flow

```
Sensor -> Preprocessing -> Inference -> Consensus -> Alert -> Storage
           |
           +-> API -> Dashboard
```

## Deployment Architecture

- Edge devices with TensorFlow Lite models
- Central MQTT broker for coordination
- Database for event storage
- REST API server
- Web dashboard for monitoring
