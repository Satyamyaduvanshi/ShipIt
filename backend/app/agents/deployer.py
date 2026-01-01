# app/agents/deployer.py
import paramiko
import io  # <--- WE ADDED THIS IMPORT

class DeployerAgent:
    def __init__(self, ssh_details):
        """
        ssh_details: dict containing {hostname, username, private_key (string)}
        """
        self.hostname = ssh_details.get('hostname')
        self.username = ssh_details.get('username')
        self.key_str = ssh_details.get('private_key')
        self.client = None

    def connect(self):
        """Establishes the SSH connection"""
        try:
            # Create SSH Client
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # --- KEY FIX STARTS HERE ---
            # Paramiko needs a file-like object, not a raw string
            if 'BEGIN' in self.key_str:
                key_file_obj = io.StringIO(self.key_str)
                pkey = paramiko.RSAKey.from_private_key(key_file_obj)
            else:
                # Assume it's a file path if no 'BEGIN' found
                pkey = paramiko.RSAKey.from_private_key_file(self.key_str)
            # ---------------------------

            print(f"🔌 Connecting to {self.username}@{self.hostname}...")
            
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=pkey,
                timeout=10,
                look_for_keys=False,  # Disable looking in ~/.ssh/
                allow_agent=False     # Disable using local SSH agent
            )
            return True
        except Exception as e:
            print(f"❌ SSH Connection Failed: {e}")
            return False

    def execute(self, command):
        """
        Runs a shell command on the remote server.
        Returns: (stdout_str, stderr_str, exit_code_int)
        """
        if not self.client:
            return "", "Not connected", -1

        try:
            print(f"💻 Executing: {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            
            # Wait for command to finish
            exit_code = stdout.channel.recv_exit_status()
            
            # Read output
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            
            return out, err, exit_code
        except Exception as e:
            return "", str(e), -1

    def close(self):
        if self.client:
            self.client.close()