#!/bin/sh

# Start the Tailscale daemon in the background
/usr/sbin/tailscaled &

# Wait for the Tailscale daemon to start
sleep 5

# Authenticate to Tailscale using an authkey
tailscale up --authkey=${TAILSCALE_AUTHKEY}

# Run the Python application
python3 /app/main.py
