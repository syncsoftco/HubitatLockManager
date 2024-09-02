import os
import subprocess
import sys

def start_tailscale(auth_key):
    print("Starting Tailscale...")

    # Authenticate and start Tailscale
    subprocess.run(["tailscale", "up", "--authkey", auth_key], check=True)

    print("Tailscale started successfully.")

def main():
    # Check if TAILSCALE_AUTHKEY is set in the environment
    auth_key = os.getenv("TAILSCALE_AUTHKEY")
    
    if auth_key:
        start_tailscale(auth_key)
    else:
        print("TAILSCALE_AUTHKEY is not set, skipping Tailscale startup.")

    # Start the Hubitat Lock Manager API
    subprocess.run([sys.executable, "-m", "hubitat_lock_manager.api"], check=True)

if __name__ == "__main__":
    main()