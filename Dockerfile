# Use the official Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# ----------------------------
# 1) Install Cloudflare WARP
#
#   - Add the Cloudflare WARP repository’s GPG key
#   - Add the Cloudflare WARP repo to apt sources
#   - Install warp-cli
#
#   NOTE: For Debian 11 (bullseye). If you are on a different
#   base distro, you will need to adjust accordingly. 
# ----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends git gnupg curl nano htop tmux && \
    curl https://pkg.cloudflareclient.com/pubkey.gpg | gpg --dearmor | \
      tee /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg >/dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ bullseye main" \
      | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends cloudflare-warp && \
    rm -rf /var/lib/apt/lists/*

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    git nano htop tmux\
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 2) Install Python dependencies
# ----------------------------
RUN pip install --no-cache-dir --upgrade pip
RUN pip install youtube-transcript-api flask

# ----------------------------
# 3) Clone your repository
# ----------------------------
#  Use a cache-bust trick so that we always pull the latest code
RUN echo $(date +%s) > /CACHE_BUST
RUN git clone https://github.com/user41pp/spleech.git .

# ----------------------------
# 4) Make startup scripts executable
# ----------------------------
RUN chmod +x /app/startup.sh
RUN chmod +x /app/startup_wrapper.sh

# Expose the Flask port
EXPOSE 5000

# ----------------------------
# (Optional) Configure WARP 
#
# You may wish to:
#   - warp-cli register
#   - warp-cli set-mode proxy
#   - warp-cli connect
#
# Instead of placing these in the Dockerfile (which can lead to
# ephemeral or build-time issues), often it’s better to run them
# in your startup script or entrypoint if WARP needs a login token
# or Zero Trust configuration. Below is an example snippet:
#
# RUN warp-cli register
# RUN warp-cli set-mode proxy
# RUN warp-cli connect
#
# You can embed those lines below, or inside startup.sh.
# ----------------------------

# Use the startup script as the default entrypoint
ENTRYPOINT ["/app/startup.sh"]

# Keep the container running unless overriden
CMD ["sleep", "inf"]
