#!/bin/bash

set -e

# 1) Start Cloudflare WARP daemon in the background
echo "Starting warp-svc in the background..."
nohup warp-svc > /dev/null 2>&1 &

# 2) Wait a moment to ensure warp-svc is running
echo "Waiting 2s to ensure warp-svc is running..."
sleep 2

# 3) Automatically accept TOS, register, and connect
warp-cli --accept-tos registration new
warp-cli --accept-tos connect

# 4) Start your primary app (Flask, etc.) using Gunicorn for production
echo "Starting Flask app with Gunicorn..."
gunicorn -w 4 -b 0.0.0.0:5000 app:app
