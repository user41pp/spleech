import requests
import argparse

def fetch_transcript(video_id, url):
    """
    Fetches the transcript for a given video ID from the specified endpoint.

    Parameters:
        video_id (str): The ID of the video for which to fetch the transcript.
        url (str): The endpoint URL.

    Returns:
        dict or None: The response JSON if successful, None otherwise.
    """
    payload = {
        "video_id": video_id
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Check if response contains JSON
        try:
            return response.json()
        except ValueError:
            print("Response is not in JSON format.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch transcript for a video.")
    parser.add_argument("--url", required=True, help="The endpoint URL.")
    parser.add_argument("--video_id", required=True, help="The video ID to fetch the transcript for.")

    args = parser.parse_args()

    print(f"Fetching transcript for video ID: {args.video_id}")

    transcript = fetch_transcript(args.video_id, args.url)

    if transcript:
        print("Success! Transcript retrieved:")
        print(transcript)
    else:
        print("Failed to retrieve the transcript.")