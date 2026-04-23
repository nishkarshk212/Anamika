#!/usr/bin/env python3
"""Test the YouTube API integration directly."""

import asyncio
import sys
sys.path.insert(0, '/Users/nishkarshkr/Desktop/anamika')

async def test_youtube_api():
    from AnnieXMedia.platforms.Youtube import YouTubeAPI
    
    youtube = YouTubeAPI()
    
    # Test with a known video
    test_video = "dQw4w9WgXcQ"
    
    print("Testing YouTube.track()...")
    try:
        details, track_id = await YouTube.track(test_video, videoid=test_video)
        print(f"✓ Track details retrieved:")
        print(f"  Title: {details.get('title')}")
        print(f"  Duration: {details.get('duration_min')}")
        print(f"  Video ID: {track_id}")
        print(f"  Thumbnail: {details.get('thumb')}")
    except Exception as e:
        print(f"✗ YouTube.track() failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Testing YouTube.download()...")
    try:
        class MockMessage:
            pass
        
        file_path, direct = await youtube.download(test_video, MockMessage(), video=False, videoid=test_video)
        if file_path:
            print(f"✓ Download successful:")
            print(f"  File path: {file_path}")
            print(f"  Direct: {direct}")
        else:
            print(f"✗ Download returned None")
    except Exception as e:
        print(f"✗ YouTube.download() failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_youtube_api())
