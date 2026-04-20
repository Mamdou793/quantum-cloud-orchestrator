# Quantum-Cloud-Orchestrator 🌌🔐

A hybrid cloud-quantum simulation tool that integrates **NVIDIA Omniverse (USD)** with **Azure Quantum**. This project demonstrates how to orchestrate parallel quantum workloads on cloud-hosted hardware (Rigetti) to drive 3D spatial simulations.

##  Features
* **Parallel Execution:** Submits asynchronous quantum circuits to Azure Quantum to bypass sequential latency.
* **Hybrid Backend:** Bridges Qiskit-based logic with the Rigetti Quantum Virtual Machine (QVM).
* **3D Orchestration:** Uses Universal Scene Description (USD) to visualize quantum state decisions in a spatial grid.
* **Cloud Architecture:** Fully decoupled environment using environment variables for secure authentication.

##  Tech Stack
* **Language:** Python 3.12+
* **Quantum:** Qiskit, Azure Quantum SDK
* **Graphics:** NVIDIA USD (pxr-core)
* **Cloud:** Microsoft Azure (QuantumArchitect-WS)

##  Quick Start
1. Set your connection string:
   `export AZURE_QUANTUM_CONNECTION_STRING="your_string"`
2. Install dependencies:
   `pip install azure-quantum[qiskit] usd-core`
3. Run the orchestrator:
   `python test_quantum.py`