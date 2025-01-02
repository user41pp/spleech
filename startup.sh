#!/bin/bash

echo "Registering WARP..."
warp-cli register
echo "Setting WARP mode to proxy..."
warp-cli set-mode proxy
echo "Connecting to WARP..."
warp-cli connect

# Start the Flask application
echo "Starting Flask app..."
python app.py
