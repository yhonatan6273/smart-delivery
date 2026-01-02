# 📦 Smart Delivery Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![React](https://img.shields.io/badge/React-18-blue)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Event_Streaming-black)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Testing](https://img.shields.io/badge/Testing-Pytest-yellow)

**Smart Delivery** is a full-stack, event-driven microservices platform designed to optimize logistics operations. It leverages Machine Learning to predict delivery ETAs in real-time based on historical data.

The system is fully containerized and orchestrated using **Kubernetes**, featuring a decoupled architecture with Apache Kafka.

<img width="1642" height="910" alt="HOME PAGE" src="https://github.com/user-attachments/assets/8cb27358-1fd2-436a-a3c1-07ec304da19b" /><img width="1895" height="962" alt="MANAGER PAGE" src="https://github.com/user-attachments/assets/9ff4e2cb-4612-4089-bc1b-b91bc149089e" />

<img width="924" height="359" alt="image" src="https://github.com/user-attachments/assets/57edcd13-779c-424c-8c99-0b3444a548e7" />

## 🏗️ Architecture

The system follows an **Event-Driven Architecture**:

* **Backend:** Python (FastAPI) - REST API & Business Logic.
* **Frontend:** React - Interactive dashboard for delivery management.
* **Database:** PostgreSQL (managed via SQLAlchemy & Alembic).
* **Message Broker:** Apache Kafka & Zookeeper (handling asynchronous tasks).
* **Machine Learning:** Custom Scikit-learn model for ETA prediction.
* **Infrastructure:** Kubernetes (K8s) with Kustomize for environment management.

---

## 🚀 Getting Started

Follow these steps to deploy the project locally using a "clean install" method.

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (Kubernetes enabled)
* [Git](https://git-scm.com/)
* [Kubectl](https://kubernetes.io/docs/tasks/tools/)

### 1. Clone the Repository
```bash
git clone https://github.com/yhonatan6273/smart-delivery.git
cd smart-delivery
```
### 2. Environment Configuration 🔐
The project includes example configuration files. You need to generate the real .env files from them.

Step A: Root Configuration
```bash
cp .env.example_main .env
```
Step B: Backend Configuration
```bash
cp backend/.env.example_backend backend/.env
```
Important: Open backend/.env and update GOOGLE_API_KEY and SECRET_KEY. The database host is pre-configured for Kubernetes (postgres-service).

Step C: Frontend Configuration
```bash
cp frontend/.env.example_frontend frontend/.env
```
Step D: Testing & Docker (Optional) If you plan to run tests (pytest) or use Docker Compose directly:
```bash
# For running tests locally
cp backend/.env.test.example backend/.env.test

# For running tests via Docker
cp backend/.env.test.docker.example backend/.env.test.docker

# For running backend via Docker Compose (non-K8s)
cp backend/.env.docker.example backend/.env.docker
```
### 3. Deploy to Kubernetes ☸️
We use Kustomize to manage namespaces and resources automatically.

Run this single command to deploy the entire stack (DB, Kafka, Backend, Frontend):
```bash
kubectl apply -k k8s/
```

### 4. Verify Installation
Check if all pods are running in the delivery-platform namespace:
```bash
kubectl get pods -n delivery-platform
```
Wait until all pods show status Running. This might take a few minutes for the first image pull.

## Alternative: Run with Docker Compose 🐳 
If you prefer to run the system without Kubernetes, you can use Docker Compose.

**1. Build and Start:**
```bash
docker-compose up --build -d
```
**2. Verify Running Containers**
Check that all services are up and running:
```bash
docker-compose ps
```
**3. Access Services (Docker Compose):**

Frontend: http://localhost:3000

Backend: http://localhost:8000

PostgreSQL: localhost:5432

**4. Stop Containers**
```bash
docker-compose down
```

## Accessing the Services🔌
Since the services are running inside the Kubernetes cluster, use Port Forwarding to access them from your local machine.

Open separate terminals for each command:

**1. Frontend UI (React):** Access directly at http://localhost:30000
*(Exposed via NodePort 30000 - no terminal command required)*

**2. Expose Backend API (FastAPI):** Access at http://localhost:8000
```bash
kubectl port-forward -n delivery-platform svc/fastapi-service 8000:80
```
**3. Expose Database (PostgreSQL):** Access at localhost:5433 (This allows local DB tools to connect without conflicting with local Postgres)
```bash
kubectl port-forward -n delivery-platform svc/postgres-service 5433:5432
```
## Usage URLs🖥️
Once port-forwarding is active, you can access the system:

Service: Frontend UI -> URL: http://localhost:30000

Service: Swagger API Docs -> URL: http://localhost:8000/docs

## Running Tests🧪
To run the integration and unit tests, ensure you have the test environment variables set up (Step 2-D).
```bash
cd backend
pytest
```
