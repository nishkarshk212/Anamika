# Authored By Certified Coders © 2025
from pyrogram.types import BotCommand
from AnnieXMedia import app
from AnnieXMedia.logging import LOGGER

# Bot commands that will show when user types /
COMMANDS = [
    # Music Commands
    BotCommand("play", "🎵 Play a song from YouTube"),
    BotCommand("vplay", "📹 Play video from YouTube"),
    BotCommand("skip", "⏭ Skip to next track"),
    BotCommand("pause", "⏸ Pause current track"),
    BotCommand("resume", "▶️ Resume paused track"),
    BotCommand("stop", "⏹ Stop playback and clear queue"),
    BotCommand("loop", "🔁 Loop current track"),
    BotCommand("seek", "🔍 Seek to specific time"),
    BotCommand("shuffle", "🔀 Shuffle the queue"),
    BotCommand("queue", "📋 Show the queue"),
    
    # Speed Control
    BotCommand("speed", "⚡ Change playback speed"),
    
    # Admin Commands
    BotCommand("auth", "👤 Authorize user to use bot"),
    BotCommand("unauth", "🚫 Remove authorized user"),
    BotCommand("authusers", "📋 List authorized users"),
    
    # Bot Commands
    BotCommand("start", "🚀 Start the bot"),
    BotCommand("help", "❓ Get help menu"),
    BotCommand("settings", "⚙️ Open bot settings"),
    BotCommand("ping", "🏓 Check bot ping"),
    BotCommand("stats", "📊 Show bot statistics"),
    BotCommand("repo", "💻 Get bot repository"),
    
    # Search Commands
    BotCommand("search", "🔍 Search YouTube videos"),
    
    # Language
    BotCommand("lang", "🌐 Change language"),
    BotCommand("language", "🌐 Change language"),
    
    # Tools Commands
    BotCommand("waifu", "🎌 Get random waifu"),
    BotCommand("upscale", "🖼 Upscale an image"),
    BotCommand("tiny", "🔍 Make sticker tiny"),
    BotCommand("stickerid", "🆔 Get sticker ID"),
    BotCommand("stdl", "📥 Download sticker"),
    BotCommand("kang", "🦘 Kang a sticker"),
    BotCommand("mmf", "✍️ Memeify text on sticker"),
    BotCommand("tr", "🌍 Translate text"),
    BotCommand("tgm", "📤 Upload to Telegraph"),
    BotCommand("phone", "📱 Get phone info"),
    BotCommand("bug", "🐛 Report a bug"),
    BotCommand("q", "💬 Create quote sticker"),
    BotCommand("couple", "💑 Couple of the day"),
    BotCommand("github", "🐙 Get GitHub user info"),
    BotCommand("speedtest", "🚀 Run speed test"),
    BotCommand("activevc", "🎤 Show active voice chats"),
    BotCommand("vc", "🎤 Show active voice chats"),
    BotCommand("reboot", "🔄 Reboot bot"),
    
    # Group Management
    BotCommand("link", "🔗 Get group invite link"),
    BotCommand("givelink", "🔗 Get temporary invite link"),
    BotCommand("leavegroup", "🚪 Leave the group"),
    BotCommand("promote", "⬆️ Promote a member"),
    BotCommand("demote", "⬇️ Demote an admin"),
    BotCommand("ban", "🔨 Ban a user"),
    BotCommand("unban", "🔓 Unban a user"),
    BotCommand("mute", "🔇 Mute a user"),
    BotCommand("unmute", "🔊 Unmute a user"),
    BotCommand("kick", "👢 Kick a user"),
    BotCommand("purge", "🧹 Delete messages"),
    BotCommand("del", "🗑 Delete a message"),
    BotCommand("zombies", "🧹 Find deleted accounts"),
    BotCommand("id", "🆔 Get user/group ID"),
    BotCommand("info", "ℹ️ Get user info"),
    BotCommand("staff", "👥 List group admins"),
    
    # Sudo Commands
    BotCommand("broadcast", "📢 Broadcast message"),
    BotCommand("gban", "🌍 Global ban user"),
    BotCommand("ungban", "🌍 Remove global ban"),
    BotCommand("block", "🚫 Block user"),
    BotCommand("unblock", "🔓 Unblock user"),
    BotCommand("autoend", "⏱ Toggle auto end"),
    BotCommand("backup", "💾 Backup data"),
    BotCommand("restart", "🔄 Restart bot"),
    
    # Fun Commands
    BotCommand("dice", "🎲 Roll a dice"),
    BotCommand("love", "💕 Love calculator"),
    BotCommand("meme", "😂 Get random meme"),
    BotCommand("truth", "🤔 Truth question"),
    BotCommand("dare", "🔥 Dare challenge"),
    BotCommand("bored", "🎯 Get activity suggestion"),
    BotCommand("anime", "🎌 Get anime info"),
    BotCommand("movie", "🎬 Get movie info"),
    
    # Utility Commands
    BotCommand("weather", "🌤 Get weather info"),
    BotCommand("ip", "🌐 Get IP info"),
    BotCommand("qr", "📱 Generate QR code"),
    BotCommand("write", "✍️ Write text beautifully"),
    BotCommand("password", "🔐 Generate password"),
    BotCommand("pypi", "📦 Search PyPI"),
    BotCommand("domain", "🌐 Check domain info"),
    BotCommand("bgremove", "🖼 Remove background"),
    BotCommand("webdl", "🌐 Download webpage"),
    BotCommand("wish", "🎉 Wish generator"),
    BotCommand("fonts", "🔤 Fancy fonts"),
    BotCommand("hexa", "🔢 Hexadecimal code"),
    BotCommand("sg", "📊 Stalk Telegram"),
]

async def set_bot_commands():
    """Set bot commands for Telegram"""
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER(__name__).info("✅ Bot commands registered successfully")
    except Exception as e:
        LOGGER(__name__).error(f"❌ Failed to set bot commands: {e}")
