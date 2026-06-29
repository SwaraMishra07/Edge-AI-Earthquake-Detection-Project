\"\"\"Sensor data simulation and acquisition module.\n\nProvides realistic seismic sensor simulation for research and testing.\nIncludes configurable noise models and event generation patterns.\n\"\"\"\n\nimport logging\nimport numpy as np\nfrom typing import Optional\n\nlogger = logging.getLogger(__name__)

def simulate_sensor_data(sample_rate: int, duration_seconds: float = 2.0) -> np.ndarray:
    total_samples = int(sample_rate * duration_seconds)
    noise = np.random.normal(0, 0.02, size=(total_samples, 3))
    # Simulate a brief seismic event in the middle of the window.
    event = np.zeros((total_samples, 3))
    mid = total_samples // 2
    spike = np.linspace(0, 2.0, num=10)
    event[mid:mid+10, 0] = spike
    return noise + event
