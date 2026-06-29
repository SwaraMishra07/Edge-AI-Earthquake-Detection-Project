"""Experiment tracking and research artifacts management.

Provides utilities for logging experiments, tracking hyperparameters,
storing model checkpoints, and maintaining research reproducibility.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

from app.config import research_config, ARTIFACTS_DIR

logger = logging.getLogger(__name__)


class ExperimentTracker:
    """Track and log experiments for research reproducibility."""
    
    def __init__(self, experiment_id: Optional[str] = None):
        """Initialize experiment tracker.
        
        Args:
            experiment_id: Unique experiment identifier
        """
        self.experiment_id = experiment_id or research_config.experiment_id
        self.experiment_dir = ARTIFACTS_DIR / self.experiment_id
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata = {
            'experiment_id': self.experiment_id,
            'created_at': datetime.now().isoformat(),
            'random_seed': research_config.random_seed,
            'model_version': getattr(research_config, 'model_version', '1.0.0'),
        }
        
        logger.info(f"Experiment tracker initialized: {self.experiment_id}")
    
    def log_hyperparameters(self, hyperparams: Dict[str, Any]) -> None:
        """Log hyperparameters for the experiment.
        
        Args:
            hyperparams: Dictionary of hyperparameter values
        """
        params_file = self.experiment_dir / "hyperparameters.json"
        with open(params_file, 'w') as f:
            json.dump(hyperparams, f, indent=2, default=str)
        logger.info(f"Logged hyperparameters: {params_file}")
    
    def log_metrics(self, metrics: Dict[str, float], stage: str = "training") -> None:
        """Log experiment metrics.
        
        Args:
            metrics: Dictionary of metric values
            stage: Training stage (training, validation, test)
        """
        metrics_file = self.experiment_dir / f"{stage}_metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                **metrics
            }, f, indent=2)
        logger.info(f"Logged {stage} metrics")
    
    def save_checkpoint(self, checkpoint_data: Dict[str, Any], name: str = "checkpoint") -> Path:
        """Save model checkpoint.
        
        Args:
            checkpoint_data: Checkpoint dictionary
            name: Checkpoint name
        
        Returns:
            Path to saved checkpoint
        """
        checkpoint_dir = self.experiment_dir / "checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)
        
        checkpoint_file = checkpoint_dir / f"{name}_{datetime.now().timestamp()}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)
        
        logger.info(f"Saved checkpoint: {checkpoint_file}")
        return checkpoint_file
    
    def get_config_hash(self) -> str:
        """Generate hash of experiment configuration.
        
        Returns:
            SHA256 hash of metadata
        """
        config_str = json.dumps(self.metadata, sort_keys=True, default=str)
        return hashlib.sha256(config_str.encode()).hexdigest()
    
    def finalize(self, results: Dict[str, Any]) -> None:
        """Finalize experiment and save results.
        
        Args:
            results: Final experiment results
        """
        results_file = self.experiment_dir / "results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'experiment_id': self.experiment_id,
                'completed_at': datetime.now().isoformat(),
                'config_hash': self.get_config_hash(),
                **results
            }, f, indent=2, default=str)
        
        logger.info(f"Experiment finalized: {results_file}")


def create_tracker(experiment_id: Optional[str] = None) -> ExperimentTracker:
    """Factory function for creating experiment tracker.
    
    Args:
        experiment_id: Optional experiment identifier
    
    Returns:
        ExperimentTracker instance
    """
    return ExperimentTracker(experiment_id)
