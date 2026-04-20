import math
import csv
import os
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from pxr import Usd, UsdGeom, Gf
from qiskit import QuantumCircuit

# 1. Identity Setup
connection_string = os.environ.get("AZURE_QUANTUM_CONNECTION_STRING")
workspace = Workspace.from_connection_string(connection_string)
provider = AzureQuantumProvider(workspace)

class QuantumOmniTool:
    ALPHA_COLOR = Gf.Vec3f(0.1, 0.8, 0.2)
    BETA_COLOR = Gf.Vec3f(0.8, 0.1, 0.1)

    def __init__(self, provider, stage_path="quantum_sim.usda"):
        self.provider = provider
        # Start with the simulator for testing
        self.backend = self.provider.get_backend("rigetti.sim.qvm")
        
        if os.path.exists(stage_path):
            self.stage = Usd.Stage.Open(stage_path)
        else:
            self.stage = Usd.Stage.CreateNew(stage_path)
            
        UsdGeom.SetStageUpAxis(self.stage, UsdGeom.Tokens.y)
        self.qubit_data = []

    def _get_quantum_decision(self, stress_factor, shielding_factor=0.0):
        qc = QuantumCircuit(1, 1)
        qc.h(0) 
        effective_stress = stress_factor * (1.0 - shielding_factor)
        theta = effective_stress * math.pi
        qc.ry(theta, 0)
        qc.measure(0, 0)
        
        # This sends the job to the Azure Cloud
        job = self.backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        measurement = list(counts.keys())[0]
        return "Beta" if measurement == "1" else "Alpha"

    def generate_grid(self, count=10, spacing=2.0):
        self.qubit_data = []
        for i in range(count):
            for j in range(count):
                path = f"/World/Qubit_{i}_{j}"
                prim = self.stage.GetPrimAtPath(path)
                if prim.IsValid():
                    cube = UsdGeom.Cube.Get(self.stage, path)
                else:
                    cube = UsdGeom.Cube.Define(self.stage, path)
                
                height = 5.0 + (i * 2.0) 
                pos = Gf.Vec3f(i * spacing, height, j * spacing)
                
                xformable = UsdGeom.Xformable(cube)
                ops = xformable.GetOrderedXformOps()
                if not ops:
                    xformable.AddTranslateOp().Set(pos)
                else:
                    ops[0].Set(pos)
                
                self.qubit_data.append({"id": f"{i}_{j}", "height": height, "path": path})
        self.stage.Save()

    def run_simulation(self, shielding=0.0, log_file="results.csv"):
            if not self.qubit_data:
                return {"Alpha": 0, "Beta": 0}

            max_h = max(d["height"] for d in self.qubit_data)
            stats = {"Alpha": 0, "Beta": 0}
            
            # 1. FIRE OFF ALL JOBS AT ONCE (Asynchronous)
            print(f"Submitting {len(self.qubit_data)} parallel jobs to Rigetti...")
            jobs = []
            for data in self.qubit_data:
                stress = (data["height"] - 5.0) / (max_h - 5.0) if max_h > 5.0 else 0
                qc = QuantumCircuit(1, 1)
                qc.h(0)
                theta = stress * (1.0 - shielding) * math.pi
                qc.ry(theta, 0)
                qc.measure(0, 0)
                
                # Submit the job but DON'T wait for it yet
                job = self.backend.run(qc, shots=1)
                jobs.append((data, job))

            # 2. COLLECT RESULTS AS THEY FINISH
            print("Waiting for all cloud results...")
            with open(log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Qubit_ID", "Fall_Height", "Resulting_State"])
                
                for data, job in jobs:
                    # This line waits for the specific job to finish
                    result = job.result()
                    counts = result.get_counts()
                    measurement = list(counts.keys())[0]
                    
                    state = "Beta" if measurement == "1" else "Alpha"
                    stats[state] += 1
                    
                    # Update USD
                    cube_prim = UsdGeom.Cube.Get(self.stage, data["path"])
                    color = Gf.Vec3f(0.1, 0.8, 0.2) if state == "Alpha" else Gf.Vec3f(0.8, 0.1, 0.1)
                    cube_prim.GetDisplayColorAttr().Set([color])
                    writer.writerow([data["id"], round(data["height"], 2), state])
            
            self.stage.Save()
            return stats