# Use the Tailscale base image
FROM tailscale/tailscale:stable

# Set the working directory
WORKDIR /app

# Install Python and required dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy the requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the application code
COPY hubitat_lock_manager /app/hubitat_lock_manager
COPY main.py /app/main.py

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the API server port
EXPOSE 5000

# Use the entrypoint script to start the Tailscale daemon and run the main.py script
ENTRYPOINT ["/app/entrypoint.sh"]
