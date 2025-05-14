#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install requirements if not already installed
pip install -r requirements.txt

# Run locust with web interface
echo "Starting Locust load testing..."
echo "Open http://localhost:8089 in your browser to access the Locust web interface"
locust -f tests/locustfile.py --host=http://localhost:8000 