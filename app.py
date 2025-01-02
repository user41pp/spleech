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

import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url_or_id):
    """
    Extracts the YouTube video ID from a URL or video ID.

    Args:
        youtube_url_or_id (str): A YouTube video URL or video ID.

    Returns:
        str: The video ID, or None if extraction fails.
    """
    # Regular expression to match a YouTube video ID
    video_id_pattern = r'^[a-zA-Z0-9_-]{11}$'  # Matches valid YouTube video IDs which are 11 characters long

    # Check if the input is already a video ID
    if re.match(video_id_pattern, youtube_url_or_id):
        return youtube_url_or_id

    # Parse the URL to extract the query parameters
    try:
        parsed_url = urlparse(youtube_url_or_id)  # Parses the URL to understand its structure and extract components
        query_params = parse_qs(parsed_url.query)

        # Extract the video ID from the "v" parameter
        if "v" in query_params:
            return query_params["v"][0]

        # Handle shortened YouTube links (youtu.be/ID)
        if parsed_url.netloc in ("youtu.be", "www.youtu.be"):  # Specifically handles shortened YouTube URLs
            return parsed_url.path.lstrip("/")

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error parsing URL: {e}")

    # Return None if the video ID couldn't be extracted
    return None

def extract_clean_text(transcript_data):
    """
    Extracts and returns the clean text from a YouTube transcript.

    Parameters:
        transcript_data (list): The transcript data containing timestamps and text.
            Expected format: [{'duration': float, 'start': float, 'text': str}, ...]

    Returns:
        str: A single string with all the transcript text concatenated and cleaned of metadata.
    """
    if not isinstance(transcript_data, list):
        raise TypeError("Input must be a list of dictionaries containing 'text' keys.")

    clean_text = ' '.join(entry['text'] for entry in transcript_data if isinstance(entry, dict) and 'text' in entry)
    return str(clean_text)


def get_transcript(youtube_url_or_video_id, retries=3, delay=2):
    video_id = extract_video_id(youtube_url_or_video_id)
    logging.debug(f"Extracted videoID: {video_id}")
    for attempt in range(retries):
        try:
            logging.debug(f"Attempt {attempt + 1} to fetch transcript for video_id={video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            logging.info(f"Successfully fetched transcript for video_id={video_id}")
            return extract_clean_text(transcript)
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

        if not video_id or not isinstance(video_id, str) or len(video_id.strip()) == 0:
            logging.error("Invalid or missing video_id")
            return jsonify({"error": "Invalid or missing video_id"}), 400

        result = get_transcript(video_id)
        if not isinstance(result, str):  # Error message
            logging.error(f"Error fetching transcript: {result}")
            return jsonify({"error": result}), 500

        logging.info(f"Transcript fetched successfully for video_id={video_id}")
        return jsonify({"transcript": result})
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected server error: {e}"}), 500

def main_cli():
    logging.debug("CLI mode called")
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript using video ID and cookies.\nExample: python app.py <video_id>")
    parser.add_argument('video_id', type=str, help="The ID of the YouTube video.")

    args = parser.parse_args()

    result = get_transcript(args.video_id)
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
