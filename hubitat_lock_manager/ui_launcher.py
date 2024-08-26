import os
import subprocess
import importlib.util
import sys

# Read the port from an environment variable
port = os.getenv("PORT", "8501")  # Default port is 8501 if not specified

# Determine the file path for the Streamlit app
module_name = "hubitat_lock_manager.ui"
spec = importlib.util.find_spec(module_name)

if spec is None:
    print(f"Cannot find module {module_name}")
    sys.exit(1)

# Get the absolute path of the .py file
file_path = spec.origin

# Construct the command to run the Streamlit script with the specified port
command = ["streamlit", "run", file_path, "--server.port", port]

# Run the command
subprocess.run(command)
