# Spleech

Spleech (SpeechLeech) is a Flask-based web application that extracts and returns YouTube video transcripts using the [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api). It is designed to be hosted on [Fly.io](https://fly.io/).

## Features
- Extracts transcripts from YouTube videos using video IDs or URLs.
- Provides a clean and concatenated transcript text.
- Includes CLI and REST API endpoints for interaction.
- Custom request session headers for better compatibility.

## Table of Contents
1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Usage](#usage)
    - [API Endpoints](#api-endpoints)
    - [CLI Usage](#cli-usage)
4. [Testing](#testing)
5. [Deployment](#deployment)

## Requirements
- Python 3.8+
- Docker (for deployment)
- [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd spleech
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Fly.io:
   - Run `flyctl launch` and follow the prompts.
   - Ensure the `fly.toml` file is correctly configured.

4. Run the application locally:
   ```bash
   python app.py
   ```

## Usage

### API Endpoints

#### 1. **Status Endpoint**
- **URL**: `/`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "status": "App is running",
      "app_name": "spleech-rough-wildflower-5228"
  }
  ```

#### 2. **Health Check**
- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
      "status": "healthy"
  }
  ```

#### 3. **Transcript Endpoint**
- **URL**: `/transcript`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "video_id": "<YouTube Video ID>"
  }
  ```
- **Response**:
  ```json
  {
      "transcript": "<Transcript Text>"
  }
  ```

### CLI Usage

Run the application in CLI mode to fetch a YouTube video transcript directly:

```bash
python app.py cli <video_id>
```

Example:
```bash
python app.py cli dQw4w9WgXcQ
```

## Testing

1. Run tests locally:
   ```bash
   ./run_test_locally.sh
   ```

2. Run tests in the deployment environment:
   ```bash
   ./run_test.sh
   ```

## Deployment

1. Build the Docker image:
   ```bash
   docker build -t spleech .
   ```

2. Deploy the app using Fly.io:
   ```bash
   ./deploy.sh
   ```

3. Verify the app status:
   ```bash
   fly status
   ```

## File Descriptions

- `app.py`: Core application logic.
- `Dockerfile`: Docker configuration for containerizing the app.
- `fly.toml`: Configuration for Fly.io deployment.
- `cookies.txt`: Placeholder for cookies (if required by YouTube API).
- `deploy.sh`: Script for deployment.
- `run_test.sh`: Script for testing in the deployment environment.
- `run_test_locally.sh`: Script for testing locally.
- `startup.sh`: Initialization script for app startup.
- `test.py`: Contains test cases for the app.

## Contributing
Feel free to fork the repository and make contributions. Submit a pull request with a detailed explanation of the changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Happy transcripting with **Spleech**!
