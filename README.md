# Clinical R&D Data Engineering Portfolio

This repository is a self-contained demonstration of end-to-end data pipeline development, highlighting **querying, aggregation, analysis, and visualization** using modern Python tooling. 

It is designed to address complex data challenges in clinical development, such as **agentic trial design** and **digital twin** telemetry.

## 🎯 Key Skills Demonstrated
* **Fluency in Structured Data (SQL):** Managed via `sqlite3`, representing structured clinical trial demographics.
* **Fluency in Unstructured Data (NoSQL):** Managed via `tinydb`, representing highly nested, semi-structured telemetry data (wearables/sensors).
* **Analytics Output:** Visualized using **Plotly Dash** to deliver interactive insights for statisticians and data scientists.
* **Modern Package Management:** Utilizes Astral's **`uv`** for lightning-fast, reproducible dependency management and environment isolation.

## 🚀 How to Run

Because this project uses `uv`, setup takes seconds and requires no manual virtual environment configuration.

1. **Install uv** (if not already installed):
   `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **Generate the mock SQL and NoSQL data:**
   `uv run src/data_pipeline.py`

3. **Launch the Plotly Dash application:**
   `uv run app.py`

4. Open `http://127.0.0.1:8050/` in your browser to view the interactive dashboards.