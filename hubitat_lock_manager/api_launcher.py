import subprocess
import time
import os

def start_tailscale_daemon():
    # Start the Tailscale daemon in the background
    subprocess.Popen(['/usr/local/bin/tailscaled'])

    # Wait for the Tailscale daemon to start
    time.sleep(5)

def bring_tailscale_interface_up(auth_key):
    # Bring the Tailscale interface up using the provided auth key
    subprocess.run(['/usr/local/bin/tailscale', 'up', '--authkey', auth_key, '--hostname', 'tailscale-gateway'])

def main():
    # Check if TAILSCALE_AUTHKEY is set in the environment
    auth_key = os.getenv("TAILSCALE_AUTHKEY")

    if auth_key:
        # Start the Tailscale daemon
        start_tailscale_daemon()
        
        # Connect to tailnet
        bring_tailscale_interface_up(auth_key)
    else:
        print("TAILSCALE_AUTHKEY is not set, skipping Tailscale startup.")

    # Start the Hubitat Lock Manager API
    subprocess.run([sys.executable, "-m", "hubitat_lock_manager.api"], check=True)

if __name__ == "__main__":
    main()
