import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = ("AIzaSyApplDKVy-jXX8bo1ah80gMu-NS92pnbxU")

def get_video_id(url: str):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_comments(video_id: str, max_results=50) -> list:
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "textFormat": "plainText",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        print(f"❌ YouTube xato: {data['error']['message']}")
        return []

    comments = []
    for item in data.get("items", []):
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(text)

    return comments