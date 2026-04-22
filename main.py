
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
from logic import QuantumOmniTool, provider
from azure.data.tables import TableClient

app = FastAPI(title="Quantum Cloud Orchestrator API")

# 1. ADD THIS HERE: Tracking variable for the frontend polling
simulation_status = {"completed": True}

# --- DASHBOARD CONFIGURATION ---
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/dashboard")
async def get_dashboard():
    return FileResponse('static/dashboard.html')

# 2. ADD THIS ROUTE: This is what your new JavaScript will call
@app.get("/simulation-status")
async def get_status():
    return simulation_status
# -------------------------------

def run_quantum_pipeline():
    # 3. UPDATE THIS: Use global to modify the status
    global simulation_status
    simulation_status["completed"] = False
    
    print("🚀 Background task started...")
    try:
        tool = QuantumOmniTool(provider=provider)
        tool.generate_grid(count=5)
        results = tool.run_simulation(shielding=0.1)
        print(f"✅ Simulation Complete: {results}")
    finally:
        # Always set to True even if the simulation fails
        simulation_status["completed"] = True

@app.get("/")
def read_root():
    return {"status": "Online", "engine": "Quantum-Orchestrator-v2"}

@app.post("/run-simulation")
async def trigger_simulation(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_quantum_pipeline)
    return {
        "message": "Quantum simulation triggered in background",
        "status": "Processing",
        "check_azure_table": "QuantumSimResults"
    }

@app.get("/results")
def get_results():
    storage_conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not storage_conn_str:
        return {"error": "Storage connection string not configured."}

    table_client = TableClient.from_connection_string(
        conn_str=storage_conn_str,
        table_name="QuantumSimResults"
    )

    try:
        entities = list(table_client.list_entities())
        sorted_entities = sorted(
            entities,
            key=lambda x: x.get('Timestamp', ''),
            reverse=True
        )

        return {
            "history": [
                {
                    "RunId": e.get("RowKey"),
                    "Timestamp": e.get("Timestamp"),
                    "Alpha": e.get("AlphaCount"),
                    "Beta": e.get("BetaCount"),
                    "Total": e.get("TotalJobs"),
                    "Shielding": e.get("Shielding"),
                    "Backend": e.get("Backend"),
                }
                for e in sorted_entities[:5]
            ]
        }
    except Exception as e:
        return {"error": str(e)}