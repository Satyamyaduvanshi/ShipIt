# ShipIt 🚀
> Your AI-powered DevOps assistant. From code to cloud, instantly.

## Problem Statement
Deploying modern web applications involves numerous complex steps, from provisioning servers and configuring security to installing dependencies and setting up web servers. This DevOps overhead is time-consuming, error-prone, and a significant distraction for developers who just want to ship their code.

## Features
**ShipIt** is an agentic AI platform designed to automate the entire deployment process.
* **Automated Server Provisioning:** Intelligently creates and configures virtual servers on cloud platforms like DigitalOcean.
* **Git Repository Deployment:** Deploys any application directly from a public GitHub repository.
* **Multi-Stack Intelligence:** Automatically analyzes a repository to detect the tech stack (Node.js, Python, Static HTML, etc.) and applies the correct deployment procedure.
* **Database Provisioning:** Detects if a project requires a database and can automatically provision a managed database instance.
* **Domain & SSL Configuration:** Configures DNS and sets up a free SSL certificate with Let's Encrypt for a custom domain.
* **CI/CD Pipeline Generation:** Can automatically create a GitHub Actions workflow to re-deploy the application on every code push.

## System Architecture
ShipIt is built on a multi-agent system to ensure modularity and reliability.

* **Orchestrator Agent:** The "manager" that receives the user's request, analyzes the project, and delegates tasks to specialized worker agents.
* **Provisioner Agent:** A specialist responsible for all interactions with the cloud provider's API (creating servers, databases, etc.).
* **Deployer Agent:** A specialist that connects to the server via SSH to handle all code deployment, dependency installation, and server configuration tasks.
* **Validator Agent:** A specialist that performs health checks to verify a successful deployment.

**Tech Stack:**
* **Backend:** Python, LangChain, Flask (for API)
* **Cloud Provider:** DigitalOcean API
* **Frontend:** TypeScript, React

## Setup & Installation
Follow these steps to set up the project locally.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/shipit.git](https://github.com/your-username/shipit.git)
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
4.  **Configure API Keys:**
    Create a `.env` file inside the `backend/` directory and add your secret keys:
    ```
    DIGITALOCEAN_API_KEY="your_digital_ocean_api_key"
    OPENAI_API_KEY="your_openai_api_key"
    ```

## Usage
To run a deployment from the command line:
```bash
cd backend
python main.py --repo [https://github.com/example/project.git](https://github.com/example/project.git)