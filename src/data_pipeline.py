import sqlite3
import pandas as pd
from tinydb import TinyDB
import random
from datetime import datetime
from pathlib import Path
import yaml

def generate_mock_data(experiment_name: str):
    """
    Generates structured and unstructured mock data partitioned by experiment and date.
    """
    # 1. Create dynamic path: data/{name}/YYYY/MM/DD
    now = datetime.now()
    year, month, day = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    
    output_dir = Path(f"data/{experiment_name}/{year}/{month}/{day}")
    
    # exist_ok=True prevents errors if you run the script multiple times a day
    output_dir.mkdir(parents=True, exist_ok=True) 
    
    print(f"\n🚀 Generating data for experiment: '{experiment_name}' at {output_dir}...")
    
    # 2. Structured Data (SQL)
    print("Generating Structured Data (SQL)...")
    db_path = output_dir / 'structured_clinical.db'
    conn = sqlite3.connect(str(db_path))
    sql_df = pd.DataFrame({
        'patient_id': range(1, 101),
        'age': [random.randint(20, 80) for _ in range(100)],
        'trial_arm': [random.choice(['Control', 'Treatment A', 'Agentic Design B']) for _ in range(100)],
        'baseline_score': [random.uniform(50.0, 100.0) for _ in range(100)]
    })
    sql_df.to_sql('patients', conn, if_exists='replace', index=False)
    conn.close()

    # 3. Unstructured Data (NoSQL)
    print("Generating Unstructured Data (NoSQL)...")
    json_path = output_dir / 'unstructured_telemetry.json'
    db = TinyDB(str(json_path))
    db.truncate()
    
    for i in range(1, 101):
        db.insert({
            'patient_id': i,
            'digital_twin_metrics': {
                'daily_steps_avg': random.randint(2000, 15000),
                'wearable_hrv': random.uniform(20.0, 80.0),
                'symptoms_logged': random.sample(['fatigue', 'nausea', 'headache', 'none'], k=random.randint(1,2))
            }
        })
        
    print(f"✅ Data generation complete for '{experiment_name}'.")


if __name__ == "__main__":
    # Dynamically read experiment names from schema.yaml
    config_path = "config/schema.yaml"
    
    try:
        with open(config_path, 'r') as file:
            schema_config = yaml.safe_load(file)
            
        if schema_config:
            # Iterate through all root-level keys in the YAML (e.g., "structured_clinical")
            for experiment_name in schema_config.keys():
                generate_mock_data(experiment_name=experiment_name)
        else:
            print(f"⚠️ Warning: {config_path} is empty or invalid.")
            
    except FileNotFoundError:
        print(f"❌ Error: {config_path} not found. Please ensure the config directory exists.")