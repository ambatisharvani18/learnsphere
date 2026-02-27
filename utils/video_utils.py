"""
LearnSphere — Video Utility Module
Searches YouTube for ML educational videos and provides embeddable content.
"""

import urllib.request
import urllib.parse
import json
import re


def search_youtube_videos(topic, max_results=3):
    """
    Search YouTube for educational videos on the given ML topic.
    Returns a list of dicts with title, url, video_id.
    Uses YouTube's public search page scraping (no API key needed).
    """
    query = f"{topic} machine learning tutorial explanation"
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode("utf-8")

        # Extract video IDs from the HTML
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)

        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)
            if len(unique_ids) >= max_results:
                break

        # Extract titles (best effort)
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)

        videos = []
        for i, video_id in enumerate(unique_ids):
            title = titles[i] if i < len(titles) else f"ML Tutorial: {topic}"
            videos.append({
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "video_id": video_id,
                "embed_url": f"https://www.youtube.com/embed/{video_id}",
            })

        return videos

    except Exception as e:
        # Fallback: return curated search links
        return _get_fallback_videos(topic)


def _get_fallback_videos(topic):
    """Fallback: return YouTube search link if scraping fails."""
    encoded = urllib.parse.quote(f"{topic} machine learning tutorial")
    return [{
        "title": f"Search YouTube: {topic} ML Tutorial",
        "url": f"https://www.youtube.com/results?search_query={encoded}",
        "video_id": None,
        "embed_url": None,
        "is_search_link": True,
    }]


def get_embed_url(video_url):
    """Convert a YouTube watch URL to an embeddable URL."""
    if "watch?v=" in video_url:
        video_id = video_url.split("watch?v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    return video_url
