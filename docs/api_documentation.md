# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Events

#### Get All Events
- **URL**: `/events`
- **Method**: GET
- **Response**: List of earthquake events

#### Get Event by ID
- **URL**: `/events/{event_id}`
- **Method**: GET
- **Response**: Event details

### Sensors

#### Get Sensor Status
- **URL**: `/sensors`
- **Method**: GET
- **Response**: List of all sensors and their status

#### Get Sensor by ID
- **URL**: `/sensors/{sensor_id}`
- **Method**: GET
- **Response**: Sensor details and readings

### Alerts

#### Get Active Alerts
- **URL**: `/alerts`
- **Method**: GET
- **Response**: List of active alerts

#### Create Alert
- **URL**: `/alerts`
- **Method**: POST
- **Body**: Alert data
- **Response**: Created alert

### System

#### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: System health status

#### Get Metrics
- **URL**: `/metrics`
- **Method**: GET
- **Response**: System metrics
