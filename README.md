# Quantum Cloud Orchestrator (PoC)

A containerized Python-based orchestrator designed to bridge Quantum Computing workflows with Cloud-Native data pipelines.

##   Overview
This solution implements an end-to-end ETL pipeline:
1. **Compute Layer**: Containerized Python 3.10 environment (Docker).
2. **Quantum Ingestion**: Asynchronous job submission to Rigetti QVM via Azure Quantum.
3. **Data Pipeline**: Automated ingestion of simulation results into Azure Table Storage.
4. **Security**: Environment-based secret management (Zero-Trust).


### Prerequisites
- Docker Desktop
- Azure Quantum Workspace
- Azure Storage Account

### Configuration
Create a `.env` file in the root directory:
```text
AZURE_QUANTUM_CONNECTION_STRING=ResourceId=/subscriptions/...
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
