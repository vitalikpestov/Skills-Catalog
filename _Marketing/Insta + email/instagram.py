"""
Instagram / Meta Graph API client.
Fetches post content (captions + video URLs) for given Instagram post URLs.
"""

import re
import os
import tempfile
import requests
from typing import Optional


class InstagramClient:
    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self, access_token: str, ig_user_id: str):
        self.access_token = access_token
        self.ig_user_id = ig_user_id

    def _get(self, endpoint: str, params: dict = None) -> dict:
        params = params or {}
        params["access_token"] = self.access_token
        resp = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        resp.raise_for_status()
        return resp.json()

    def _extract_shortcode(self, url: str) -> Optional[str]:
        """Extract the shortcode from an Instagram post URL."""
        patterns = [
            r"instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)",
            r"instagram\.com/reels/([A-Za-z0-9_-]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _get_all_media(self) -> list[dict]:
        """Fetch recent media from the Instagram account (up to 100 posts)."""
        data = self._get(
            f"/{self.ig_user_id}/media",
            params={
                "fields": "id,permalink,caption,media_type,timestamp",
                "limit": 100,
            },
        )
        return data.get("data", [])

    def _get_video_url(self, media_id: str) -> Optional[str]:
        """Fetch the video URL for a specific media item."""
        try:
            data = self._get(f"/{media_id}", params={"fields": "video_url"})
            return data.get("video_url")
        except Exception:
            return None

    def get_posts_by_urls(self, urls: list[str]) -> list[dict]:
        """
        Given a list of Instagram post URLs, return the post data for each.
        Returns a list of dicts with keys: url, type, caption, video_url, timestamp
        """
        shortcodes = {self._extract_shortcode(url): url for url in urls if self._extract_shortcode(url)}
        if not shortcodes:
            raise ValueError("No valid Instagram URLs found.")

        print(f"Fetching media list from Instagram account...")
        all_media = self._get_all_media()

        results = []
        matched_shortcodes = set()

        for media in all_media:
            permalink = media.get("permalink", "")
            shortcode = self._extract_shortcode(permalink)
            if shortcode and shortcode in shortcodes:
                media_type = media.get("media_type")
                video_url = self._get_video_url(media["id"]) if media_type == "VIDEO" else None
                results.append({
                    "url": shortcodes[shortcode],
                    "type": media_type,
                    "caption": media.get("caption", ""),
                    "video_url": video_url,
                    "timestamp": media.get("timestamp"),
                })
                matched_shortcodes.add(shortcode)

        unmatched = set(shortcodes.keys()) - matched_shortcodes
        if unmatched:
            unmatched_urls = [shortcodes[sc] for sc in unmatched]
            print(f"Warning: Could not find these posts in the account's recent media:")
            for u in unmatched_urls:
                print(f"  {u}")

        return results

    def download_video(self, video_url: str) -> str:
        """Download a video to a temp file, return the temp file path."""
        print(f"Downloading video...")
        resp = requests.get(video_url, stream=True)
        resp.raise_for_status()

        tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        for chunk in resp.iter_content(chunk_size=8192):
            tmp.write(chunk)
        tmp.close()
        return tmp.name
