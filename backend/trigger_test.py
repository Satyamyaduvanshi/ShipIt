import requests
import os
import random

# Base URL
API_URL = "http://127.0.0.1:5000/api"

def run_test():
    # 1. SETUP: Read PEM Key
    try:
        key_path = os.path.abspath("shipit.pem")
        with open(key_path, 'r') as f:
            private_key = f.read()
    except FileNotFoundError:
        print("❌ Error: 'shipit.pem' not found! Make sure it exists.")
        return

    # 2. AUTH: Register a fresh user
    # We use random numbers so we don't get "User already exists" errors if you run this twice.
    rand_id = random.randint(1000, 9999)
    email = f"test{rand_id}@shipit.dev"
    password = "password123"
    
    print(f"👤 Registering new user: {email}...")
    auth_resp = requests.post(f"{API_URL}/auth/register", json={
        "username": f"TestUser{rand_id}",
        "email": email,
        "password": password
    })
    
    if auth_resp.status_code != 201:
        print(f"❌ Registration Failed: {auth_resp.text}")
        # Try logging in if user already exists
        if "already exists" in auth_resp.text:
            print("🔄 User exists, trying to login...")
        else:
            return

    # 3. LOGIN: Get the Real ID
    print("🔑 Logging in to get User ID...")
    login_resp = requests.post(f"{API_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if login_resp.status_code != 200:
        print(f"❌ Login Failed: {login_resp.text}")
        return

    user_id = login_resp.json()['user_id']
    print(f"✅ Authenticated! Real User ID: {user_id}")

    # 4. DEPLOY: Send Payload with Valid ID
    payload = {
        "user_id": user_id,  # <--- USING REAL DB ID NOW
        "repo_url": "https://github.com/vercel/next-learn-starter.git",
        "ssh_details": {
            "hostname": "13.127.127.133",  # CHECK YOUR AWS IP!
            "username": "ubuntu",
            "private_key": private_key
        }
    }

    print("🚀 Sending deployment request...")
    deploy_resp = requests.post(f"{API_URL}/deploy/", json=payload)
    
    print(f"Status: {deploy_resp.status_code}")
    print(f"Response: {deploy_resp.json()}")

if __name__ == "__main__":
    run_test()