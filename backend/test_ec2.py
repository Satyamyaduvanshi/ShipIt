from app.agents.deployer import DeployerAgent
import os

# Get the absolute path to the key we just created
key_path = os.path.abspath("shipit.pem")

# Read the key content
with open(key_path, 'r') as f:
    private_key_content = f.read()

ssh_details = {
    "hostname": "13.204.82.215",  # Your AWS IP
    "username": "ubuntu",         # Default user for Ubuntu EC2
    "private_key": private_key_content
}

print(f"🔑 Using Key: {key_path}")
print(f"🔌 Connecting to AWS EC2 ({ssh_details['hostname']})...")

agent = DeployerAgent(ssh_details)

if agent.connect():
    print("✅ SUCCESS: SSH Connection Established!")
    
    # Run a test command
    print("running 'whoami'...")
    out, err, code = agent.execute("whoami")
    print(f"👤 User: {out}")  # Should print 'ubuntu'
    
    print("running 'ls -la'...")
    out, err, code = agent.execute("ls -la")
    print(f"Tb Files:\n{out}")

    agent.close()
else:
    print("❌ CONNECTION FAILED.")
    print("Tip: Check if your AWS Security Group allows Port 22 from your IP.")