import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def ingest_website(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)

def ingest_youtube(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])
