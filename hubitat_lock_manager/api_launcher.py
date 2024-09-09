import subprocess
import time
import os

def main():
    # Start the Hubitat Lock Manager API
    subprocess.run([sys.executable, "-m", "hubitat_lock_manager.api"], check=True)

if __name__ == "__main__":
    main()
