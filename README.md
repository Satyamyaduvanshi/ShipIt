# ShipIt 🚀

> Your AI-powered DevOps assistant. From code to cloud, instantly.

## Problem Statement

Deploying modern web applications involves numerous complex steps, from provisioning servers and configuring networks to installing dependencies and setting up web servers. This DevOps overhead is time-consuming, error-prone, and a significant distraction for developers who just want to ship their code.

## Features

**ShipIt** is an agentic AI platform designed to automate the entire deployment lifecycle, from simple static sites to complex, multi-service applications.

* **User Accounts & History:** Register and log in to manage your deployments and view your project history.
* **Automated AWS Provisioning:** Intelligently creates and configures EC2 instances on AWS, including necessary security groups and networking.
* **Multi-Instance Deployments:** Analyzes complex repositories and can provision separate EC2 instances for frontend and backend services.
* **Multi-Stack Intelligence:** Automatically analyzes a repository to detect the tech stack (Node.js, Python, etc.) and applies the correct deployment procedure.
* **Resilient Self-Correction:** The core of ShipIt. The agent can diagnose and recover from common deployment errors without human intervention.
* **Live Deployment Logs:** Watch the entire deployment process in real-time through a live log streamed directly to your browser.
* **CI/CD Pipeline Generation:** After a successful deployment, the agent can commit a GitHub Actions workflow file back to your repository to enable continuous deployment on future code pushes.

## System Architecture

ShipIt is built on a scalable, asynchronous architecture to handle multiple concurrent deployments reliably.

1.  **Frontend:** A user logs in via the **Next.js** web interface and submits a deployment request.
2.  **Web Server:** A **Flask** API receives the request and, instead of running the deployment itself, it creates a job and places it onto a **Redis** queue.
3.  **Task Queue:** **Celery** workers, running as separate background processes, pick up jobs from the queue.
4.  **Agent AI:** The worker invokes the **Orchestrator Agent**. This agent analyzes the project, creates a plan (e.g., "This needs two servers"), and delegates tasks to its specialist agents (Provisioner, Deployer) to execute the deployment on AWS.
5.  **Real-time Feedback:** Throughout the process, the agent sends status updates back to the user's browser via **WebSockets**.

## Tech Stack

* **Frontend:** Next.js (TypeScript)
* **Backend:** Python, Flask, Celery, WebSockets
* **AI:** LangChain, Llama 3 (or other open-source LLM)
* **Database:** PostgreSQL
* **Cloud:** AWS (using the Boto3 SDK)
* **Message Broker:** Redis

ShipIt is built on a scalable, asynchronous architecture to handle multiple concurrent deployments reliably.

1.  **Frontend:** A user logs in via the **Next.js** web interface and submits a deployment request.
2.  **Web Server:** A **Flask** API receives the request and, instead of running the deployment itself, it creates a job and places it onto a **Redis** queue.
3.  **Task Queue:** **Celery** workers, running as separate background processes, pick up jobs from the queue.
4.  **Agent AI:** The worker invokes the **Orchestrator Agent**. This agent analyzes the project, creates a plan (e.g., "This needs two servers"), and delegates tasks to its specialist agents (Provisioner, Deployer) to execute the deployment on AWS.
5.  **Real-time Feedback:** Throughout the process, the agent sends status updates back to the user's browser via **WebSockets**.

## Tech Stack

* **Frontend:** Next.js (TypeScript)
* **Backend:** Python, Flask, Celery, WebSockets
* **AI:** LangChain, Llama 3 (or other open-source LLM)
* **Database:** PostgreSQL
* **Cloud:** AWS (using the Boto3 SDK)
* **Message Broker:** Redis

## Setup & Installation

Follow these steps to set up the project locally.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Satyamyaduvanshi/ShipIt.git
    cd shipit
    ```
2.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    ```
4.  **Configure Environment Variables:**
    Create a `.env` file inside the `backend/` directory and add your secret keys:
    ```
    # AWS Credentials
    AWS_ACCESS_KEY_ID="your_aws_access_key"
    AWS_SECRET_ACCESS_KEY="your_aws_secret_key"

    # Database Connection
    DATABASE_URL="postgresql://user:password@host:port/dbname"

    # LLM API Key (from Groq, Replicate, etc.)
    LL_API_KEY="your_llm_api_key"
    ```

## Usage

After setting up the environment, you can run the frontend and backend servers separately.

* **Run Backend:**
    ```bash
    cd backend
    flask run
    # In a separate terminal, run the Celery worker
    celery -A your_app.celery worker --loglevel=info
    ```
* **Run Frontend:**
    ```bash
    cd frontend
    npm run dev
    ```
```eof
