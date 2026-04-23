#!/bin/bash
# Fix youtube-search-python async compatibility issue
# Run this after every deployment or pip install

echo "🔧 Fixing youtube-search-python async compatibility..."

VENV_DIR="/opt/AnnieXMusic/venv"
AIO_FILE="$VENV_DIR/lib/python3.10/site-packages/youtubesearchpython/aio.py"

# Create the async compatibility shim
cat > "$AIO_FILE" << 'PYEOF'
"""Async compatibility layer for youtube-search-python 1.5.x"""
from youtubesearchpython import VideosSearch as SyncVideosSearch, Playlist as SyncPlaylist
import asyncio
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=4)

class VideosSearch:
    def __init__(self, query, limit=20, region=None, language=None, timeout=None):
        self.query = query
        self.limit = limit
        self.region = region
        self.language = language
        self.timeout = timeout
        self._sync = SyncVideosSearch(query, limit=limit, region=region, language=language)
    
    async def next(self):
        """Async wrapper for sync search"""
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(_executor, lambda: self._sync.result())
            return result
        except Exception as e:
            return {"result": []}

class Playlist:
    def __init__(self, name, link=None, timeout=None):
        self.name = name
        self.link = link
        self.timeout = timeout
        if link:
            self._sync = SyncPlaylist(name=link, link=link)
        else:
            self._sync = SyncPlaylist(name=name)
    
    async def next(self):
        """Async wrapper for sync playlist"""
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(_executor, lambda: self._sync.result())
            return result
        except Exception as e:
            return {"result": []}
PYEOF

echo "✅ Async compatibility shim installed at: $AIO_FILE"
echo "✅ You can now restart the bot"
