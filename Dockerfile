# Use the official Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    git nano htop\
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository into the working directory
RUN git clone https://github.com/user41pp/spleech.git .

# Install Python dependencies if any (youtube-dl doesn't have a requirements.txt but for extensibility)
RUN pip install --no-cache-dir --upgrade pip

RUN pip install youtube-transcript-api flask

# Make the startup script executable
RUN chmod +x /app/startup.sh

# Expose the Flask port
EXPOSE 5000

# Use the startup script as the default entrypoint
ENTRYPOINT ["/app/startup.sh"]

# Set the default command to run the Flask app
CMD ["sleep", "inf"]
