import sqlite3
import pandas as pd
from tinydb import TinyDB
import random
from datetime import datetime
from pathlib import Path

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
    
    print(f"Generating data for experiment: '{experiment_name}' at {output_dir}...")
    
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
    # Example execution for a specific trial
    generate_mock_data(experiment_name="trial_alpha")