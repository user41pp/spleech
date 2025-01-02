from flask import Flask, request, jsonify
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import time
import os
import logging
import requests

# Create a custom session
custom_session = requests.Session()
custom_session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.84 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    # Add any other headers you need here
})

# Monkey-patch the library’s private session to use our custom session
YouTubeTranscriptApi._YouTubeTranscriptApi__session = custom_session


# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def get_transcript(video_id, cookies_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            logging.debug(f"Attempt {attempt + 1} to fetch transcript for video_id={video_id} with cookies at {cookies_path}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=cookies_path)
            logging.info(f"Successfully fetched transcript for video_id={video_id}")
            return transcript
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                logging.error(f"All retries failed for video_id={video_id}")
                return str(e)

@app.route('/')
def status():
    logging.debug("Status endpoint called")
    return jsonify({"status": "App is running", "app_name": "spleech-rough-wildflower-5228"})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/transcript', methods=['POST'])
def fetch_transcript():
    logging.debug("Transcript endpoint called")
    try:
        data = request.get_json()
        logging.debug(f"Received request data: {data}")
        video_id = data.get('video_id')
        cookies = data.get('cookies')

        if not video_id or not isinstance(video_id, str) or len(video_id.strip()) == 0:
            logging.error("Invalid or missing video_id")
            return jsonify({"error": "Invalid or missing video_id"}), 400

        if not cookies or not isinstance(cookies, str) or len(cookies.strip()) == 0:
            logging.error("Invalid or missing cookies")
            return jsonify({"error": "Invalid or missing cookies"}), 400

        # Write cookies to a file
        cookies_path = os.path.join(os.getcwd(), 'cookies.txt')
        logging.debug(f"Writing cookies to file at {cookies_path}")
        try:
            with open(cookies_path, 'w') as f:
                f.write(cookies)
        except Exception as e:
            logging.error(f"Failed to write cookies file: {e}")
            return jsonify({"error": f"Failed to write cookies file: {e}"}), 500

        # Use the path to cookies.txt in get_transcript
        result = get_transcript(video_id, cookies_path)
        if isinstance(result, str):  # Error message
            logging.error(f"Error fetching transcript: {result}")
            return jsonify({"error": result}), 500

        logging.info(f"Transcript fetched successfully for video_id={video_id}")
        return jsonify({"transcript": result})
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected server error: {e}"}), 500

def main_cli():
    logging.debug("CLI mode called")
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript using video ID and cookies.\nExample: python script.py <video_id> <cookies>")
    parser.add_argument('video_id', type=str, help="The ID of the YouTube video.")
    parser.add_argument('cookies', type=str, help="The cookies string to authenticate requests.")

    args = parser.parse_args()

    # Write cookies to a file
    cookies_path = os.path.join(os.getcwd(), 'cookies.txt')
    logging.debug(f"Writing cookies to file at {cookies_path}")
    try:
        with open(cookies_path, 'w') as f:
            f.write(args.cookies)
    except Exception as e:
        logging.error(f"Failed to write cookies file: {e}")
        return

    result = get_transcript(args.video_id, cookies_path)
    if isinstance(result, str):  # Error message
        logging.error(f"Error: {result}")
    else:
        logging.info(f"Transcript fetched successfully: {result}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        main_cli()
    else:
        logging.debug("Starting Flask server")
        app.run(host='0.0.0.0', port=5000)
