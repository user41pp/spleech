from flask import Flask, request, jsonify
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import time

app = Flask(__name__)

def get_transcript(video_id, cookies, retries=3, delay=2):
    for attempt in range(retries):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=cookies)
            return transcript
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                return str(e)

@app.route('/transcript', methods=['POST'])
def fetch_transcript():
    data = request.get_json()
    video_id = data.get('video_id')
    cookies = data.get('cookies')

    if not video_id or not isinstance(video_id, str) or len(video_id.strip()) == 0:
        return jsonify({"error": "Invalid or missing video_id"}), 400

    if not cookies or not isinstance(cookies, str) or len(cookies.strip()) == 0:
        return jsonify({"error": "Invalid or missing cookies"}), 400

    result = get_transcript(video_id, cookies)
    if isinstance(result, str):  # Error message
        return jsonify({"error": result}), 500
    
    return jsonify({"transcript": result})

@app.route('/')
def status():
    return jsonify({"status": "App is running", "app_name": "spleech-rough-wildflower-5228"})

def main_cli():
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcript using video ID and cookies.\nExample: python script.py <video_id> <cookies>")
    parser.add_argument('video_id', type=str, help="The ID of the YouTube video.")
    parser.add_argument('cookies', type=str, help="The cookies string to authenticate requests.")

    args = parser.parse_args()

    result = get_transcript(args.video_id, args.cookies)
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
