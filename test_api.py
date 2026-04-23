#!/usr/bin/env python3
"""Test NubCoder API to check if it's working correctly."""

import requests

API_KEY = "wym8vakam2"
API_URL = "http://api.nubcoder.com"

# Test video info endpoint
test_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

print(f"Testing NubCoder API...")
print(f"API URL: {API_URL}")
print(f"API Key: {API_KEY}")
print()

# Test 1: Get video info
print("Test 1: Getting video info...")
try:
    response = requests.get(
        f'{API_URL}/info',
        params={'token': API_KEY, 'q': test_video, 'max_results': 1},
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 2: Search videos
print("Test 2: Searching videos...")
try:
    response = requests.get(
        f'{API_URL}/search',
        params={'q': 'Never Gonna Give You Up', 'max_results': 1},
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 3: Rate limit status
print("Test 3: Rate limit status...")
try:
    response = requests.get(
        f'{API_URL}/rate-limit-status',
        params={'token': API_KEY},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
