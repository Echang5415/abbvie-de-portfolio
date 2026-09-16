import sqlite3
import pandas as pd
from tinydb import TinyDB
import random

def generate_mock_data():
    # 1. Structured Data (SQL): Clinical Trial Demographics
    print("Generating Structured Data (SQL)...")
    conn = sqlite3.connect('data/structured_clinical.db')
    sql_df = pd.DataFrame({
        'patient_id': range(1, 101),
        'age': [random.randint(18, 80) for _ in range(100)],
        'trial_arm': [random.choice(['Control', 'Treatment']) for _ in range(100)],
        'baseline_score': [random.uniform(50.0, 100.0) for _ in range(100)]
    })
    sql_df.to_sql('patients', conn, if_exists='replace', index=False)
    conn.close()

    print("Generating Unstructured Data (NoSQL)...")
    # 2. Unstructured/Semi-Structured Data (NoSQL): Patient Notes and Telemetry
    db = TinyDB('data/unstructured_telemetry.json')
    db.truncate()
    for i in range(1, 101):
        db.insert({
            'patient_id': i,
            'telemetry_metrics': {
                'daily_steps_avg': random.randint(2000, 15000),
                'wearable_hrv': random.uniform(20.0, 80.0),
                'symptoms_logged': random.sample(['fatigue', 'nausea', 'headache', 'none'], k=random.randint(1,2))
            }
        })
    print("Mock data generation complete.")

if __name__ == "__main__":
    generate_mock_data()