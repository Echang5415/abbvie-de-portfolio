import yaml
import pandas as pd

def load_yaml(file_path: str) -> dict:
    """Reads a YAML configuration file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_schema(df: pd.DataFrame, config_path: str, dataset_name: str):
    """Validates dataframe columns and datatypes against a YAML schema."""
    config = load_yaml(config_path)
    schema = config.get(dataset_name, {})
    
    if not schema:
        raise ValueError(f"Dataset '{dataset_name}' not found in schema config.")

    # 1. Check for missing columns
    missing_cols = set(schema.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Schema Validation Failed: Missing columns {missing_cols} in {dataset_name}")

    # 2. Check datatypes
    for col, expected_type in schema.items():
        actual_type = str(df[col].dtype)
        if actual_type != expected_type:
            raise TypeError(
                f"Schema Validation Failed: Column '{col}' is type '{actual_type}', expected '{expected_type}'"
            )
    print(f"✅ Schema validation passed for {dataset_name}.")

def validate_values(df: pd.DataFrame, config_path: str, dataset_name: str):
    """Validates data values based on rules (min, max, allowed values) in a YAML file."""
    config = load_yaml(config_path)
    rules = config.get(dataset_name, {})

    if not rules:
        print(f"⚠️ No validation rules found for {dataset_name}. Skipping value checks.")
        return

    for col, rule in rules.items():
        if col not in df.columns:
            continue
            
        # Check Minimums
        if 'min' in rule:
            if not (df[col] >= rule['min']).all():
                bad_data = df[df[col] < rule['min']][col].tolist()
                raise ValueError(f"Value Validation Failed: '{col}' contains values below minimum {rule['min']}. Found: {bad_data}")
        
        # Check Maximums
        if 'max' in rule:
            if not (df[col] <= rule['max']).all():
                bad_data = df[df[col] > rule['max']][col].tolist()
                raise ValueError(f"Value Validation Failed: '{col}' contains values above maximum {rule['max']}. Found: {bad_data}")
        
        # Check Allowed Categorical Values
        if 'allowed_values' in rule:
            invalid_mask = ~df[col].isin(rule['allowed_values'])
            if invalid_mask.any():
                bad_data = df[invalid_mask][col].unique().tolist()
                raise ValueError(f"Value Validation Failed: '{col}' contains unauthorized values: {bad_data}. Allowed: {rule['allowed_values']}")
                
    print(f"✅ Value validation passed for {dataset_name}.")