#  Quantum Cloud Orchestrator

An end-to-end cloud-native pipeline for orchestrating quantum simulations. This project bridges classical FastAPI compute with Azure Quantum, utilizing a reactive dashboard for real-time monitoring.

##  Architecture
- **Backend:** FastAPI (Python) with asynchronous background task management.
- **Frontend:** HTML5/JavaScript with Chart.js for live data visualization.
- **Infrastructure:** Containerized via Docker and deployed on Azure Container Apps (UK South).
- **Data Layer:** Azure Table Storage for persistent simulation history.
- **Quantum Layer:** Azure Quantum / QDK for quantum state generation.

##  Key Features
- **Asynchronous Processing:** Triggers long-running quantum jobs without blocking the UI.
- **Stateful Polling:** Frontend automatically detects job completion via a polling mechanism.
- **Cloud Scale:** Fully serverless deployment with automated scaling and private registry security.

##  Deployment
1. **Build & Tag:**
   `docker build -t <registry-url>/quantum-api:v3 .`
2. **Push to Registry:**
   `docker push <registry-url>/quantum-api:v3`
3. **Azure Update:**
   `az containerapp update --name <app-name> --image <image-v3>`

##  Dashboard
The dashboard provides a historical view of Alpha and Beta quantum states, allowing for immediate verification of cloud-quantum job outcomes.

<img width="938" height="616" alt="Screenshot 2026-04-22 at 9 39 47 PM" src="https://github.com/user-attachments/assets/ee630323-10d4-4013-b1a3-8c6adbffe22b" />
