
import json

class DiagnoserAgent:
    def __init__(self, use_llm=False):
        self.use_llm = use_llm

    def detect_stack(self, file_list, package_json_content=None):
        """
        Analyzes the file structure to identify the Tech Stack.
        """
        print(f"🧠 AI Analyzing Project Structure...")

        
        if 'package.json' in file_list:
            print("🧠 Detected Node.js Project")
            install_cmd = "npm install"
            start_cmd = "node index.js"
            
           
            if package_json_content:
                try:
                    pkg = json.loads(package_json_content)
                    scripts = pkg.get('scripts', {})
                    

                    if 'dev' in scripts:
                        start_cmd = "npm run dev"
                    elif 'start' in scripts:
                        start_cmd = "npm start"
                        
                    print(f"🧠 AI determined start command: '{start_cmd}'")
                except:
                    pass

            return {
                "type": "node",
                "install_cmd": install_cmd,
                "start_cmd": start_cmd
            }

        if 'requirements.txt' in file_list:
            print("🧠 Detected Python Project")
            return {
                "type": "python",
                "install_cmd": "pip install -r requirements.txt",
                "start_cmd": "python app.py"
            }

        return None

    def diagnose(self, error_log):
        """
        Analyzes runtime errors to suggest fixes.
        """
        print("🧠 AI Diagnosing error...")

        if "npm: command not found" in error_log:
            return {
                "cause": "Node.js/NPM missing.",
                "fix_command": "sudo apt-get update && sudo apt-get install -y nodejs npm",
                "description": "Installing Node.js Environment."
            }
        
        if "Address already in use" in error_log:
            return {
                "cause": "Port blocked.",
                "fix_command": "npx kill-port 3000",
                "description": "Killing blocking process."
            }

        if "MODULE_NOT_FOUND" in error_log:
            return {
                "cause": "Wrong entry file.",
                "fix_command": "npm run dev",
                "description": "Switching to 'npm run dev'."
            }

        return {"fix_command": None}