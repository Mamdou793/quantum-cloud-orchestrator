from fastapi import FastAPI, BackgroundTasks
import os
import uuid
from logic import QuantumOmniTool, provider
from azure.data.tables import TableClient

app = FastAPI(title="Quantum Cloud Orchestrator API")

def run_quantum_pipeline():
    print(" Background task started...")

    tool = QuantumOmniTool(provider=provider)
    tool.generate_grid(count=5)
    results = tool.run_simulation(shielding=0.1)

    print(f" Simulation Complete: {results}")

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
                    "RunId": e.get("RunId"),
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
