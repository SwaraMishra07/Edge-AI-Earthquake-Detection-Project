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
        \n        Args:\n            metrics: Dictionary of metric values\n            stage: Training stage (training, validation, test)\n        \"\"\"\n        metrics_file = self.experiment_dir / f\"{stage}_metrics.json\"\n        with open(metrics_file, 'w') as f:\n            json.dump({\n                'timestamp': datetime.now().isoformat(),\n                **metrics\n            }, f, indent=2)\n        logger.info(f\"Logged {stage} metrics\")\n    \n    def save_checkpoint(self, checkpoint_data: Dict[str, Any], name: str = \"checkpoint\") -> Path:\n        \"\"\"Save model checkpoint.\n        \n        Args:\n            checkpoint_data: Checkpoint dictionary\n            name: Checkpoint name\n        \n        Returns:\n            Path to saved checkpoint\n        \"\"\"\n        checkpoint_dir = self.experiment_dir / \"checkpoints\"\n        checkpoint_dir.mkdir(exist_ok=True)\n        \n        checkpoint_file = checkpoint_dir / f\"{name}_{datetime.now().timestamp()}.json\"\n        with open(checkpoint_file, 'w') as f:\n            json.dump(checkpoint_data, f, indent=2, default=str)\n        \n        logger.info(f\"Saved checkpoint: {checkpoint_file}\")\n        return checkpoint_file\n    \n    def get_config_hash(self) -> str:\n        \"\"\"Generate hash of experiment configuration.\n        \n        Returns:\n            SHA256 hash of metadata\n        \"\"\"\n        config_str = json.dumps(self.metadata, sort_keys=True, default=str)\n        return hashlib.sha256(config_str.encode()).hexdigest()\n    \n    def finalize(self, results: Dict[str, Any]) -> None:\n        \"\"\"Finalize experiment and save results.\n        \n        Args:\n            results: Final experiment results\n        \"\"\"\n        results_file = self.experiment_dir / \"results.json\"\n        with open(results_file, 'w') as f:\n            json.dump({\n                'experiment_id': self.experiment_id,\n                'completed_at': datetime.now().isoformat(),\n                'config_hash': self.get_config_hash(),\n                **results\n            }, f, indent=2, default=str)\n        \n        logger.info(f\"Experiment finalized: {results_file}\")\n\n\ndef create_tracker(experiment_id: Optional[str] = None) -> ExperimentTracker:\n    \"\"\"Factory function for creating experiment tracker.\n    \n    Args:\n        experiment_id: Optional experiment identifier\n    \n    Returns:\n        ExperimentTracker instance\n    \"\"\"\n    return ExperimentTracker(experiment_id)
