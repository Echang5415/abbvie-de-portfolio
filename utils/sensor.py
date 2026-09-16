import os
from pathlib import Path
from utils.logger import get_pipeline_logger

# Initialize logger
logger = get_pipeline_logger(logger_name="DataSensor")

def validate_data_readiness(experiment_name: str, year: str, month: str, day: str) -> Path:
    """
    Sensor function that verifies the data directory exists before pipeline execution.
    Returns the resolved Path if successful, otherwise raises an exception.
    """
    target_dir = Path(f"data/{experiment_name}/{year}/{month}/{day}")
    
    logger.info(f"Sensing data directory: {target_dir}")
    
    if not target_dir.exists():
        error_msg = f"Sensor Failed: Data dependency missing. Expected directory not found: {target_dir}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    success_msg = f"Sensor passed: Data found at {target_dir}"
    print(f"✅ {success_msg}")
    logger.info(success_msg)
    
    return target_dir