# Authored By Certified Coders © 2025
import asyncio
from typing import Union

from AnnieXMedia.misc import db
from AnnieXMedia.utils.formatters import check_duration, seconds_to_min
from AnnieXMedia.logging import LOGGER
from config import autoclean, time_to_seconds

# Background download tracking
_background_downloads = {}
_download_lock = asyncio.Lock()


async def put_queue(
    chat_id,
    original_chat_id,
    file,
    title,
    duration,
    user,
    vidid,
    user_id,
    stream,
    forceplay: Union[bool, str] = None,
):
    title = title.title()
    try:
        duration_in_seconds = time_to_seconds(duration) - 3
    except:
        duration_in_seconds = 0
    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "user_id": user_id,
        "chat_id": original_chat_id,
        "file": file,
        "vidid": vidid,
        "seconds": duration_in_seconds,
        "played": 0,
    }
    if forceplay:
        check = db.get(chat_id)
        if check:
            check.insert(0, put)
        else:
            db[chat_id] = []
            db[chat_id].append(put)
    else:
        db[chat_id].append(put)
    autoclean.append(file)
    
    # Start background download for queued YouTube videos
    if "vid_" in str(file) and vidid and vidid not in _background_downloads:
        asyncio.create_task(_download_in_background(vidid, title))


async def put_queue_index(
    chat_id,
    original_chat_id,
    file,
    title,
    duration,
    user,
    vidid,
    stream,
    forceplay: Union[bool, str] = None,
):
    if "20.212.146.162" in vidid:
        try:
            dur = await asyncio.get_event_loop().run_in_executor(
                None, check_duration, vidid
            )
            duration = seconds_to_min(dur)
        except:
            duration = "ᴜʀʟ sᴛʀᴇᴀᴍ"
            dur = 0
    else:
        dur = 0
    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "chat_id": original_chat_id,
        "file": file,
        "vidid": vidid,
        "seconds": dur,
        "played": 0,
    }
    if forceplay:
        check = db.get(chat_id)
        if check:
            check.insert(0, put)
        else:
            db[chat_id] = []
            db[chat_id].append(put)
    else:
        db[chat_id].append(put)


async def _download_in_background(vidid: str, title: str):
    """Download video in background while current song is playing"""
    async with _download_lock:
        if vidid in _background_downloads:
            return
        _background_downloads[vidid] = True
    
    try:
        from AnnieXMedia import YouTube
        
        LOGGER(__name__).info(f"⚡ Background caching started: {title}")
        
        # Download the file in background
        file_path, direct = await YouTube.download(
            vidid,
            None,  # No mystic message for background downloads
            videoid=True,
            video=False,  # Default to audio for faster download
        )
        
        if file_path:
            LOGGER(__name__).info(f"✅ Background caching completed: {title}")
        else:
            LOGGER(__name__).debug(f"Background caching skipped (using stream): {title}")
    except Exception as e:
        LOGGER(__name__).debug(f"Background caching error for {title}: {e}")
    finally:
        async with _download_lock:
            _background_downloads.pop(vidid, None)
