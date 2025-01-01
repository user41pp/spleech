from flask import Flask, request, jsonify
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import time
import os

app = Flask(__name__)

def get_transcript(video_id, cookies_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=cookies_path)
            return transcript
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                return str(e)

@app.route('/')
def status():
    return jsonify({"status": "App is running", "app_name": "spleech-rough-wildflower-5228"})

@app.route('/transcript', methods=['POST'])
def fetch_transcript():
    data = request.get_json()
    video_id = data.get('video_id')
    cookies = data.get('cookies')

    if not video_id or not isinstance(video_id, str) or len(video_id.strip()) == 0:
        return jsonify({"error": "Invalid or missing video_id"}), 400

    if not cookies or not isinstance(cookies, str) or len(cookies.strip()) == 0:
        return jsonify({"error": "Invalid or missing cookies"}), 400

    # Write cookies to a file
    cookies_path = os.path.join(os.getcwd(), 'cookies.txt')
    try:
        with open(cookies_path, 'w') as f:
            f.write(cookies)
    except Exception as e:
        return jsonify({"error": f"Failed to write cookies file: {e}"}), 500

    # Use the path to cookies.txt in get_transcript
    result = get_transcript(video_id, cookies_path)
    if isinstance(result, str):  # Error message
        return jsonify({"error": result}), 500
    
    return jsonify({"transcript": result})

def main_cli():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript using video ID and cookies.\nExample: python script.py <video_id> <cookies>")
    parser.add_argument('video_id', type=str, help="The ID of the YouTube video.")
    parser.add_argument('cookies', type=str, help="The cookies string to authenticate requests.")

    args = parser.parse_args()

    # Write cookies to a file
    cookies_path = os.path.join(os.getcwd(), 'cookies.txt')
    try:
        with open(cookies_path, 'w') as f:
            f.write(args.cookies)
    except Exception as e:
        print(f"Failed to write cookies file: {e}")
        return

    result = get_transcript(args.video_id, cookies_path)
    if isinstance(result, str):  # Error message
        print(f"Error: {result}")
    else:
        print(result)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        main_cli()
    else:
        app.run(host='0.0.0.0', port=5000)
