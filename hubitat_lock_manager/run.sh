#!/bin/bash

# Start the Flask API in the background in development mode with auto-reload
echo "Starting Flask API in development mode with auto-reload..."
export FLASK_APP=api.py
export FLASK_ENV=development
nohup flask run > flask_api.log 2>&1 &

# Get the PID of the Flask process
FLASK_PID=$!
echo "Flask API started with PID $FLASK_PID"

# Wait for a moment to ensure the server has started
sleep 2

# Extract the address from the log file
FLASK_ADDRESS=$(grep -oP '(?<=Running on ).*' flask_api.log | head -1)

# Check if the Flask address was determined
if [ -z "$FLASK_ADDRESS" ]; then
    echo "Unable to determine Flask API address. Check flask_api.log for details."
    kill $FLASK_PID
    echo "Flask API process $FLASK_PID has been terminated."
    exit 1
fi

# Print the address of the Flask server
echo "Flask API is running at $FLASK_ADDRESS"

# Start the Streamlit application
echo "Starting Streamlit application..."
nohup streamlit run ui.py > streamlit_app.log 2>&1 &

# Get the PID of the Streamlit process
STREAMLIT_PID=$!
echo "Streamlit application started with PID $STREAMLIT_PID"

# Function to stop both processes
function stop_processes {
    echo "Stopping Flask API and Streamlit application..."
    kill $FLASK_PID
    kill $STREAMLIT_PID
    echo "Processes stopped."
}

# Trap SIGINT and SIGTERM to stop both processes
trap stop_processes SIGINT SIGTERM

# Wait for both processes to finish
wait $FLASK_PID
wait $STREAMLIT_PID
