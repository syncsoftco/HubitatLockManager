import os
import subprocess

# Read the port from an environment variable
port = os.getenv("PORT", "8501")  # Default port is 8501 if not specified

# Construct the command to run the Streamlit module with the specified port
command = ["python", "-m", "streamlit", "run", "hubitat_lock_manager.ui", "--server.port", port]

# Run the command
subprocess.run(command)
