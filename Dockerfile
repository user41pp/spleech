# Use the official Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    git nano htop tmux\
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies if any (youtube-dl doesn't have a requirements.txt but for extensibility)
RUN pip install --no-cache-dir --upgrade pip

RUN pip install youtube-transcript-api flask

# Clone the GitHub repository into the working directory. Print date to always clone newest version.
RUN echo $(date +%s) > /CACHE_BUST
RUN git clone https://github.com/user41pp/spleech.git .

# Make the startup script executable
RUN chmod +x /app/startup.sh
RUN chmod +x /app/startup_wrapper.sh

# Expose the Flask port
EXPOSE 5000

# Use the startup script as the default entrypoint
ENTRYPOINT ["/app/startup.sh"]

# Set the default command to run the Flask app
CMD ["sleep", "inf"]
