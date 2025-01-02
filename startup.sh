#!/bin/bash
set -e

# 1) Start Cloudflare WARP daemon in the background
nohup warp-svc > /dev/null 2>&1 &

# 2) Wait a moment to ensure warp-svc is running
sleep 2

# 3) Automatically accept TOS, register, and connect
#    (If "warp-cli register --accept-tos" is sufficient for you, use that)
yes y | warp-cli registration new --accept-tos
warp-cli mode proxy
warp-cli connect

# 4) Start your primary app (Flask, etc.)
#    Use 'exec' so your process gets signals directly
echo "Starting Flask app..."
exec python app.py