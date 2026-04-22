#  Quantum-Cloud-Orchestrator (Phase 3)

A cloud-native middleware service that orchestrates quantum circuit execution on **Azure Quantum** and persists stateful environmental data using **OpenUSD**.

##  Architecture
- **API Framework:** FastAPI (Asynchronous logic)
- **Quantum Backend:** Azure Quantum (Rigetti/IonQ)
- **Data Layer:** Azure Table Storage
- **Scene Description:** Pixar OpenUSD (Geometric state persistence)
- **Deployment:** Docker (Multi-stage builds for security/efficiency)

##  Key Features
- **Decoupled Processing:** Uses FastAPI BackgroundTasks to handle high-latency quantum jobs without blocking the client.
- **Stateful History:** Real-time ingestion of simulation results into Azure Cloud.
- **Architectural Scalability:** Containerized design ready for Azure App Service or Kubernetes (AKS).

##  Getting Started

### Prerequisites
- Docker
- Azure Quantum Workspace
- Azure Storage Account

### Running the Service
1. **Build the image:**
   ```bash
   docker build -t quantum-api:v1 .

2.  **Launch the container:**
docker run -p 8000:8000 --env-file .env quantum-api:v1

Navigate to http://localhost:8000/docs to interact with the API via Swagger UI.