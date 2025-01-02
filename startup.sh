#!/bin/bash

set -e

# Start Cloudflare WARP daemon
#nohup warp-svc > /dev/null 2>&1 &
#echo "Starting warp-svc in the background..."
#sleep 2

# Register and connect to WARP
#warp-cli register --accept-tos || echo "WARP registration failed or already registered."
#warp-cli connect || echo "WARP connection failed. Continuing without WARP."

# 1) Start Cloudflare WARP daemon in the background
#nohup warp-svc > /dev/null 2>&1 &

# 2) Wait a moment to ensure warp-svc is running
#sleep 2

# 3) Automatically accept TOS, register, and connect
#    (If "warp-cli register --accept-tos" is sufficient for you, use that)
#yes y | warp-cli registration new --accept-tos
#warp-cli mode proxy
#warp-cli connect

# 4) Start your primary app (Flask, etc.)
#    Use 'exec' so your process gets signals directly
#echo "Starting Flask app..."
#python app.py