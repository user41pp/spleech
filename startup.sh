#!/bin/bash

set -e

# 1) Start Cloudflare WARP daemon in the background

echo "Starting warp-svc in the background..."
nohup warp-svc > /dev/null 2>&1 &

# 2) Wait a moment to ensure warp-svc is running
echo "Waiting 5s to ensure warp-svc is running..."
sleep 5

# 3) Automatically accept TOS, register, and connect
yes y | warp-cli registration new
warp-cli connect

# 4) Start your primary app (Flask, etc.)
echo "Starting Flask app..."
python app.py