import logging
from logging.handlers import TimedRotatingFileHandler
import os

def get_pipeline_logger(logger_name="DataPipelineLogger", log_file="pipeline.log"):
    """
    Configures and returns a logger that rotates daily and retains 30 days of history.
    """
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger(logger_name)
    
    # Prevent adding duplicate handlers if this function is called multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Setup file handler: Rotate at midnight, keep 30 backups
        filepath = os.path.join('logs', log_file)
        handler = TimedRotatingFileHandler(filepath, when='midnight', backupCount=30)
        handler.setLevel(logging.INFO)
        
        # Define the log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger