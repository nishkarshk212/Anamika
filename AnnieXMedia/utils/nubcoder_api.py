# Authored By Certified Coders © 2025
import requests
from typing import List, Dict, Optional, Tuple
from config import API_KEY, API_URL

BASE_URL = API_URL or 'http://api.nubcoder.com'
API_TOKEN = API_KEY

def get_video_info(url_or_query: str, max_results: int = 1) -> Dict:
    """
    Get video info from NubCoder API
    Returns dict with: title, video_id, duration, youtube_link, channel_name, views, url, thumbnail, time_taken
    """
    try:
        response = requests.get(
            f'{BASE_URL}/info',
            params={'token': API_TOKEN, 'q': url_or_query, 'max_results': max_results},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return {'error': data.get('error')}
        
        return {
            'title': data.get('title', 'N/A'),
            'video_id': data.get('video_id', 'N/A'),
            'duration': data.get('duration', 0),
            'youtube_link': data.get('youtube_link', 'N/A'),
            'channel_name': data.get('channel_name', 'N/A'),
            'views': data.get('views', 0),
            'url': data.get('url', 'N/A'),
            'thumbnail': data.get('thumbnail', 'N/A'),
            'time_taken': data.get('time_taken', 'N/A')
        }
    except requests.RequestException as e:
        return {'error': str(e)}

def search_videos(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search videos from NubCoder API
    Returns list of dicts with: title, video_id, channel_name, duration, views, youtube_link
    """
    try:
        response = requests.get(
            f'{BASE_URL}/search',
            params={'token': API_TOKEN, 'q': query, 'max_results': max_results},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return []
        
        results = []
        for video in data.get('results', []):
            results.append({
                'title': video.get('title', 'N/A'),
                'video_id': video.get('video_id', 'N/A'),
                'channel_name': video.get('channel_name', 'N/A'),
                'duration': video.get('duration', 0),
                'views': video.get('views', 0),
                'youtube_link': video.get('youtube_link', 'N/A')
            })
        return results
    except requests.RequestException as e:
        return []

def get_rate_limit_status() -> Dict:
    """
    Get quota status from NubCoder API
    Returns dict with: daily_limit, requests_used, requests_remaining, is_admin, reset_time
    """
    try:
        response = requests.get(
            f'{BASE_URL}/rate-limit-status',
            params={'token': API_TOKEN},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            'daily_limit': data.get('daily_limit', 0),
            'requests_used': data.get('requests_used', 0),
            'requests_remaining': data.get('requests_remaining', 0),
            'is_admin': data.get('is_admin', False),
            'reset_time': data.get('reset_time', 'N/A')
        }
    except requests.RequestException as e:
        return {'error': str(e)}
