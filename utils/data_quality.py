import yaml
import pandas as pd

from utils.logger import get_pipeline_logger

# Initialize the logger using our new module
logger = get_pipeline_logger(logger_name="DataQuality")

def load_yaml(file_path: str) -> dict:
    """Reads a YAML configuration file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_schema(df: pd.DataFrame, config_path: str, dataset_name: str):
    """Validates dataframe columns and datatypes against a YAML schema."""
    config = load_yaml(config_path)
    schema = config.get(dataset_name, {})
    
    if not schema:
        error_msg = f"Dataset '{dataset_name}' not found in schema config."
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 1. Check for missing columns
    missing_cols = set(schema.keys()) - set(df.columns)
    if missing_cols:
        error_msg = f"Schema Validation Failed: Missing columns {missing_cols} in {dataset_name}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 2. Check datatypes
    for col, expected_type in schema.items():
        actual_type = str(df[col].dtype)
        if actual_type != expected_type:
            error_msg = f"Schema Validation Failed: Column '{col}' is type '{actual_type}', expected '{expected_type}'"
            logger.error(error_msg)
            raise TypeError(error_msg)
            
    success_msg = f"Schema validation passed for {dataset_name}."
    print(f"✅ {success_msg}")
    logger.info(success_msg)

def validate_values(df: pd.DataFrame, config_path: str, dataset_name: str):
    """Validates data values based on rules (min, max, allowed values) in a YAML file."""
    config = load_yaml(config_path)
    rules = config.get(dataset_name, {})

    if not rules:
        warn_msg = f"No validation rules found for {dataset_name}. Skipping value checks."
        print(f"⚠️ {warn_msg}")
        logger.warning(warn_msg)
        return

    for col, rule in rules.items():
        if col not in df.columns:
            continue
            
        # Check Minimums
        if 'min' in rule:
            if not (df[col] >= rule['min']).all():
                bad_data = df[df[col] < rule['min']][col].tolist()
                error_msg = f"Value Validation Failed: '{col}' contains values below minimum {rule['min']}. Found: {bad_data}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        # Check Maximums
        if 'max' in rule:
            if not (df[col] <= rule['max']).all():
                bad_data = df[df[col] > rule['max']][col].tolist()
                error_msg = f"Value Validation Failed: '{col}' contains values above maximum {rule['max']}. Found: {bad_data}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        # Check Allowed Categorical Values
        if 'allowed_values' in rule:
            invalid_mask = ~df[col].isin(rule['allowed_values'])
            if invalid_mask.any():
                bad_data = df[invalid_mask][col].unique().tolist()
                error_msg = f"Value Validation Failed: '{col}' contains unauthorized values: {bad_data}. Allowed: {rule['allowed_values']}"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
    success_msg = f"Value validation passed for {dataset_name}."
    print(f"✅ {success_msg}")
    logger.info(success_msg)