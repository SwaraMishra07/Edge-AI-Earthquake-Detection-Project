# Research Notes

## Earthquake Detection Techniques

### Seismic Wave Analysis
- P-waves (Primary): Fast but less destructive
- S-waves (Secondary): Slower but more destructive
- Surface waves: Cause most damage

### Machine Learning Approach
- Real-time time-series classification
- Convolutional Neural Networks (CNN) for pattern recognition
- Edge deployment with quantized models

## Model Development

### Dataset
- USGS earthquake data
- Regional seismic network data
- Synthetic data generation

### Preprocessing
- Bandpass filtering (0.1-25 Hz)
- Normalization by 9.8 m/s²
- Sliding window approach

### Feature Engineering
- Frequency domain features (FFT)
- Time-domain features (RMS, peak value)
- Wavelet coefficients

## References

- USGS Earthquake Hazards Program
- IRIS Seismic Data Management Center
- IEEE Earthquake Early Warning Systems

## Performance Metrics

- Detection latency: <2 seconds
- False positive rate: <1%
- Model accuracy: >95%
