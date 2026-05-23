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

### System Architecture 🏗️
<img width="100%" alt="System Architecture" src="https://github.com/user-attachments/assets/c09eb0cf-dbf3-426a-ae32-849976f54785" />


### Demo Video 🎥
[▶️ Click here to watch the project demo](https://github.com/user-attachments/assets/ee38c840-ff0d-45d8-a9ce-5f2d6aa17340)


### UI Screenshots 💻

**Manager Dashboard**
<img width="100%" alt="MANAGER PAGE" src="https://github.com/user-attachments/assets/2dfbf96d-d1a6-4f24-9a60-666ccceaaaca" />

**Home Page**
<img width="100%" alt="HOME PAGE" src="https://github.com/user-attachments/assets/74dedd60-69e2-4ea3-9971-d2e00f0783ba" />


 
## Architecture Overview

The system follows an **Event-Driven Architecture**:

* **Backend:** Python (FastAPI) - REST API & Business Logic.
* **Frontend:** React - Interactive dashboard for delivery management.
* **Database:** PostgreSQL (managed via SQLAlchemy & Alembic).
* **Message Broker:** Apache Kafka & Zookeeper (handling asynchronous tasks).
* **Machine Learning:** Custom Scikit-learn model for ETA prediction.
* **Infrastructure:** Kubernetes (K8s) with Kustomize for environment management.

---

## Getting Started  🚀 

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

**Step A: Root Configuration (only for docker)**
```bash
cp .env.example_main .env
```
> **Important:** Open `.env` and update `GOOGLE_API_KEY`.
> 
**Step B: Backend Configuration**
```bash
cp backend/.env.example_backend backend/.env
```
> **Important:** Open `backend/.env` and update `GOOGLE_API_KEY` and `SECRET_KEY`. The database host is pre-configured for Kubernetes (`postgres-service`).

**Step C: Frontend Configuration (only for docker)**
```bash
cp frontend/.env.example_frontend frontend/.env
```
**Step D: Testing & Docker (Optional)**
If you plan to run tests (pytest) or use Docker Compose directly:
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
```bash
cd backend
```
**Run this single command inside backend**
```bash
cp backend/k8s/secrets.yaml.template  backend/k8s/secrets.yaml
```
> **Important:** Open `secrets.yaml` and update `GOOGLE_API_KEY` , `SECRET_KEY` ,`POSTGRES_PASSWORD`,`DATABASE_URL`


**Run this single command to deploy the entire stack (DB, Kafka, Backend, Frontend):**
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

* Frontend: http://localhost:3000
* Kafka UI (Akhq): http://localhost:8080

**4. Stop Containers**
```bash
docker-compose down
```

## Accessing the Services from Kubernetes 🔌
Since the services are running inside the Kubernetes cluster, use Port Forwarding to access them from your local machine.

Open separate terminals for each command:

**1. Frontend UI (React):** Access directly at http://localhost:30000
*(Exposed via NodePort 30000 - no terminal command required)*

**3. Expose Database (PostgreSQL):** Access at localhost:5433 (This allows local DB tools to connect without conflicting with local Postgres)
```bash
kubectl port-forward -n delivery-platform svc/postgres-service 5433:5432
```
**4. Expose Kafka Url (Akhq):** Access at localhost:30080
```bash
kubectl port-forward -n delivery-platform svc/akhq-service 30080:8080
```

## Summary of URLs 🖥️
| Service | URL |
|---------|-----|
| **Frontend UI** | http://localhost:30000 |
| **Kafka UI** | http://localhost:30080 |


## Setting Up Admin Access 👑
By default, every new user is registered with a `user` role. To access the **Manager Dashboard** and view, delete, or edit all deliveries, you need to manually upgrade a user to `admin`.

**1. Register a new user** via the React UI (Register Page).

**2. Connect to the Database:**
You can use any SQL client (like DBeaver/pgAdmin) connecting to `localhost:5433` (if port-forwarded), or run this command directly inside the Kubernetes pod:

```bash

kubectl exec -it $POD_NAME -n delivery-platform -- psql -U postgres -d deliveries_database_k8s
```
**3. Update the User Role:**
Run the following SQL query inside the pod (replace `your_email@example.com` with your registered email):
```sql
UPDATE users SET role = 'admin' WHERE email = 'your_email@example.com';
 Verify the change:
SELECT * FROM users WHERE email = 'your_email@example.com';
Exit psql:
\q
```
Now refresh the website go to home page login in again to the user, and you will see the "Manager" tab in the navigation bar.
## Running Tests 🧪
To run the integration and unit tests, you must first spin up the test environment (Test DB & Kafka).

**1. Start the Test Infrastructure:**
Run this command from the root directory to build and start the test containers :
```bash
docker-compose -f docker-compose.test.yml up -d --build
```
> **Note:** Ensure your `.env.test` files are configured correctly as shown in step 2-D and all the containers are up.

**2. Run the Tests:** Go to the root(smart-delivery) and run the test suite inside the containerized environment using the test runner:

```bash
docker compose -f docker-compose.test.yml run --rm runner pytest
```

**3. Cleanup (Optional):**
After finishing the tests, you can stop the test environment:
```bash
docker-compose -f docker-compose.test.yml down
```
