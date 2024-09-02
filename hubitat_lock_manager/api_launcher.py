import os
import subprocess
import sys

def start_tailscaled():
    print("Starting tailscaled...")
    subprocess.run(["tailscaled", "--state", "/var/lib/tailscale/tailscaled.state"], check=True)
    print("tailscaled started successfully.")

def start_tailscale(auth_key):
    print("Starting Tailscale...")
    subprocess.run(["tailscale", "up", "--authkey", auth_key], check=True)
    print("Tailscale started successfully.")

def main():
    # Check if TAILSCALE_AUTHKEY is set in the environment
    auth_key = os.getenv("TAILSCALE_AUTHKEY")

    if auth_key:
        # Start the Tailscale daemon
        start_tailscaled()
        
        # Connect to tailnet
        start_tailscale(auth_key)
    else:
        print("TAILSCALE_AUTHKEY is not set, skipping Tailscale startup.")

    # Start the Hubitat Lock Manager API
    subprocess.run([sys.executable, "-m", "hubitat_lock_manager.api"], check=True)

if __name__ == "__main__":
    main()
