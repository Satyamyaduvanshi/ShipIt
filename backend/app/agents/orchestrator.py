# app/agents/orchestrator.py
from app.agents.deployer import DeployerAgent
from app.agents.diagnoser import DiagnoserAgent
import time

class OrchestratorAgent:
    def __init__(self, deployment_id, repo_url, ssh_details, socketio):
        self.deployment_id = deployment_id
        self.repo_url = repo_url
        self.socketio = socketio
        self.deployer = DeployerAgent(ssh_details)
        self.diagnoser = DiagnoserAgent()

    def log(self, message, level="info"):
        print(f"[{level.upper()}] {message}")
        self.socketio.emit('log', {
            'deployment_id': self.deployment_id,
            'message': message,
            'level': level,
            'timestamp': time.time()
        })

    def run(self):
        self.log("🚀 Orchestrator started.")
        
        # 1. CONNECT
        self.log("🔌 Connecting to server...")
        if not self.deployer.connect(): return False

        # 2. CLEAN & CLONE
        self.log("Mw Cleaning previous deployment...")
        self.deployer.execute("rm -rf app")
        
        self.log(f"📦 Cloning {self.repo_url}...")
        _, _, code = self.deployer.execute(f"git clone {self.repo_url} app")
        if code != 0: return False

        # --- 🧠 STEP 3: IDENTIFY PROJECT AI ---
        self.log("🧠 Analyzing project structure...")
        
        # A. List files to detect language
        files_str, _, _ = self.deployer.execute("ls app")
        file_list = files_str.split('\n')
        
        # B. Read package.json for specific scripts
        pkg_content = None
        if 'package.json' in file_list:
            pkg_content, _, _ = self.deployer.execute("cat app/package.json")

        # C. AI Decision
        stack_info = self.diagnoser.detect_stack(file_list, pkg_content)
        
        if not stack_info:
            self.log("❌ AI could not identify project type.", "error")
            return False

        self.log(f"✅ Identified {stack_info['type'].upper()} Project.", "success")
        install_cmd = f"cd app && {stack_info['install_cmd']}"
        start_cmd = f"cd app && timeout 10 {stack_info['start_cmd']}"
        # --------------------------------------

        # 4. INSTALL (Dynamic)
        self.log(f"🛠️ Installing: {stack_info['install_cmd']}...")
        _, err, code = self.deployer.execute(install_cmd)
        
        if code != 0:
            # Trigger Self-Healing if install fails (e.g. missing Node)
            if self.attempt_fix(err, install_cmd):
                pass
            else:
                return False

        # 5. START (Dynamic)
        self.log(f"🚀 Starting: {stack_info['start_cmd']}...")
        _, err, code = self.deployer.execute(start_cmd)
        
        if code == 124 or code == 0:
            self.log("✅ Application started successfully!", "success")
            return True
        else:
            self.log(f"❌ Start Failed: {err}", "error")
            return False

    def attempt_fix(self, error_log, retry_command):
        diagnosis = self.diagnoser.diagnose(error_log)
        if not diagnosis['fix_command']: return False
        
        self.log(f"🧠 AI identified issue: {diagnosis['cause']}", "info")
        self.log(f"🚑 Applying Fix: {diagnosis['description']}", "warning")
        
        _, _, fix_code = self.deployer.execute(diagnosis['fix_command'])
        
        if fix_code == 0:
            self.log("✅ Fix applied! Retrying...", "success")
            _, _, retry_code = self.deployer.execute(retry_command)
            return retry_code == 0
        return False
        
    def cleanup(self):
        self.deployer.close()