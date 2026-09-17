# --- NEW: Dynamically read EXPERIMENT from schema.yaml ---
import yaml

def get_experiment_name(config_path="config/schema.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        if config:
            # Get the first top-level key (e.g., 'structured_clinical')
            return list(config.keys())[0] 
    raise ValueError("Schema config is empty or invalid.")
