"""Machine learning inference engine for earthquake detection.

Provides model loading, inference execution, and performance tracking
for research-based model evaluation and optimization.
"""

import logging
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
except ImportError:
    tf = None
    logger.warning("TensorFlow not available - inference disabled")

from app.config import model_config


class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass


def load_model(model_file: str = "earthquake_model.tflite") -> Optional[object]:
    """Load TensorFlow Lite model from disk.
    
    Args:
        model_file: Model filename in models directory
    
    Returns:
        TFLite interpreter or None if load fails
    
    Raises:
        ModelLoadError: If model file not found or load fails
    """
    if tf is None:
        logger.error("TensorFlow not available")
        return None
    
    model_path = Path(model_config.model_path.parent) / model_file
    
    if not model_path.exists():
        raise ModelLoadError(f"Model not found: {model_path}")
    
    try:
        interpreter = tf.lite.Interpreter(model_path=str(model_path))
        interpreter.allocate_tensors()
        logger.info(f"Model loaded: {model_path} (v{model_config.model_version})")
        return interpreter
    except Exception as e:
        raise ModelLoadError(f"Failed to load model: {e}") from e


def run_inference(
    interpreter: object,
    features: np.ndarray,
    return_metadata: bool = False,
) -> Tuple[float, Optional[Dict[str, Any]]] | float:
    """Run inference on input features.
    
    Args:
        interpreter: TFLite interpreter instance
        features: Input feature vector (must match model input shape)
        return_metadata: Whether to return prediction metadata
    
    Returns:
        Tuple of (prediction_score, metadata_dict) if return_metadata=True
        else just prediction_score
    """
    if interpreter is None:
        logger.warning("Interpreter not initialized")
        return (0.5, None) if return_metadata else 0.5
    
    try:
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        sample = features.astype(np.float32).reshape(1, -1)
        interpreter.set_tensor(input_details[0]["index"], sample)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])
        score = float(output_data[0][0])
        
        if return_metadata:
            metadata = {
                'model_version': model_config.model_version,
                'input_shape': input_details[0]['shape'].tolist(),
            }
            logger.debug(f"Inference complete: score={score:.4f}")
            return score, metadata
        
        return score
        
    except Exception as e:
        logger.error(f"Inference failed: {e}", exc_info=True)
        return (0.5, None) if return_metadata else 0.5
