import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3
from tinydb import TinyDB
from datetime import datetime
import yaml

from utils.sensor import validate_data_readiness
from utils.data_quality import validate_schema, validate_values
from utils.helpers import get_experiment_name

# 1. Define the parameters for the current run
EXPERIMENT = get_experiment_name()
now = datetime.now()
YEAR, MONTH, DAY = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")

# 2. TRIGGER SENSOR: If this fails, the app stops immediately
data_dir = validate_data_readiness(EXPERIMENT, YEAR, MONTH, DAY)

# --- 1. QUERYING & VALIDATION ---
def load_and_query_data():
    # Query Structured Data (SQL) - Updated to use dynamic data_dir
    conn = sqlite3.connect(str(data_dir / 'structured_clinical.db'))
    sql_df = pd.read_sql("SELECT * FROM patients WHERE age >= 25", conn)
    conn.close()
    
    # Run Quality Checks on SQL Data - Updated to use dynamic EXPERIMENT variable
    print(f"Running Quality Checks on SQL Data for {EXPERIMENT}...")
    validate_schema(sql_df, 'config/schema.yaml', EXPERIMENT)
    validate_values(sql_df, 'config/validations.yaml', EXPERIMENT)
    
    # Query Unstructured Data (NoSQL) - Updated to use dynamic data_dir
    db = TinyDB(str(data_dir / 'unstructured_telemetry.json'))
    nosql_data = db.all()
    
    nosql_df = pd.json_normalize(nosql_data)
    nosql_df.rename(columns={
        'digital_twin_metrics.daily_steps_avg': 'steps', 
        'digital_twin_metrics.wearable_hrv': 'hrv'
    }, inplace=True)
    
    merged_df = pd.merge(sql_df, nosql_df, on='patient_id')
    return merged_df

df = load_and_query_data()

# --- 2. AGGREGATION AND ANALYSIS ---
# Aggregate baseline scores by trial 
agg_df = df.groupby('trial_arm')['baseline_score'].mean().reset_index()
agg_df = agg_df.round(2)

# --- 3. VISUALIZATION ---
# Bar Chart: Aggregate SQL Data
fig_bar = px.bar(
    agg_df,
    x='trial_arm',
    y='baseline_score',
    title='Average Baseline Score by Trial Arm',
    labels={'trial_arm': 'Trial Arm', 'baseline_score': 'Average Baseline Score'},
    color='trial_arm'
)

# Scatter Plot: Merged SQL and NoSQL data
fig_scatter = px.scatter(
    df, 
    x='age', 
    y='steps', 
    color='trial_arm', 
    size='hrv',
    title="Digital Twin Telemetry: Age vs Daily Steps (SQL + NoSQL)",
    labels={'age': 'Patient Age', 'steps': 'Avg Daily Steps'}
)

# --- DASH APP LAYOUT ---
app = dash.Dash(__name__)
app.title = "AbbVie Data Engineering Portfolio"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '40px'}, children=[
    html.H1("Clinical R&D Data Engineering Pipeline"),
    html.P(f"An end-to-end demonstration of processing, merging, and visualizing structured (SQL) and unstructured (NoSQL) data for digital twin modeling. Current Experiment: {EXPERIMENT}"),
    
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '30px'}, children=[
        dcc.Graph(figure=fig_bar, style={'flex': '1', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'}),
        dcc.Graph(figure=fig_scatter, style={'flex': '1', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'})
    ])
])

if __name__ == '__main__':
    # Run using: uv run app.py
    app.run(debug=True, use_reloader=False)