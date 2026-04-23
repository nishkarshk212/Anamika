#!/usr/bin/env python3
"""Test the API directly to see exact response."""

import requests

API_KEY = "wym8vakam2"
API_URL = "http://api.nubcoder.com"

test_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

print("Testing /info endpoint...")
response = requests.get(
    f'{API_URL}/info',
    params={'token': API_KEY, 'q': test_video, 'max_results': 1},
    timeout=30
)

print(f"Status: {response.status_code}")
data = response.json()

print(f"\nAll keys in response:")
for key in data.keys():
    print(f"  - {key}")

print(f"\nChecking for URL fields:")
print(f"  'url' present: {'url' in data}")
print(f"  'stream_url' present: {'stream_url' in data}")

if 'url' in data:
    print(f"  'url' value: {data['url'][:100]}..." if data['url'] and len(data['url']) > 100 else f"  'url' value: {data['url']}")

if 'stream_url' in data:
    print(f"  'stream_url' value: {data['stream_url'][:100]}..." if data['stream_url'] and len(data['stream_url']) > 100 else f"  'stream_url' value: {data['stream_url']}")

print(f"\nFull response (first 500 chars):")
import json
print(json.dumps(data, indent=2)[:500])
