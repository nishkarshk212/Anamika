# Enhanced Broadcast Feature Documentation

## Overview
The broadcast system has been enhanced to support:
- ✅ Text messages
- ✅ Images with captions
- ✅ Inline buttons (URL buttons)
- ✅ Interactive setup process

## Commands

### 1. `/broadcast` (Original Command)
The original broadcast command remains unchanged.

**Usage:**
```
/broadcast <message> [-pin] [-pinloud] [-nobot] [-user] [-assistant]
```

**Flags:**
- `-pin` - Pin the message in chats (silent)
- `-pinloud` - Pin the message with notification
- `-nobot` - Don't broadcast to bots
- `-user` - Broadcast to individual users
- `-assistant` - Broadcast via assistant accounts

---

### 2. `/newbroadcast` (New Command)
Starts an interactive broadcast setup panel that guides you through the process.

**Usage:**
```
/newbroadcast
```

This command shows you instructions on how to format your broadcast content.

---

### 3. `/setbroadcast` (New Command)
Sets the broadcast content by replying to a message.

**Usage:**
1. Create a message with your content
2. Reply to that message with `/setbroadcast`

**Supported Formats:**

#### A. Text Only
Simply send a text message and reply with `/setbroadcast`

#### B. Image with Caption
Send a photo with a caption, then reply with `/setbroadcast`

#### C. With Inline Buttons
Format your message text using the pipe (`|`) separator:

```
Your message text | Button Text 1:URL1 | Button Text 2:URL2
```

**Examples:**

1. **Text with buttons:**
   ```
   📢 Important Announcement! Join our channels for updates. | Support Group:t.me/support | News Channel:t.me/channel | YouTube:https://youtube.com
   ```

2. **Image with caption and buttons:**
   - Send a photo with caption:
   ```
   🎵 New Music Feature Available! Try it now. | Try Now:t.me/bot?start=help | Support:t.me/support
   ```
   - Reply with `/setbroadcast`

---

### 4. `/startbroadcast` (New Command)
Starts the broadcast with the content you set using `/setbroadcast`.

**Usage:**
```
/startbroadcast [flags]
```

**Flags:**
- `-pin` - Pin the message in chats (silent)
- `-pinloud` - Pin the message with notification
- `-nobot` - Don't broadcast to bots
- `-user` - Broadcast to individual users

**Examples:**
```
/startbroadcast                  # Broadcast to all chats
/startbroadcast -user            # Broadcast to users only
/startbroadcast -pin             # Broadcast and pin in chats
/startbroadcast -pinloud -user   # Broadcast to users with pinned messages
```

---

## Step-by-Step Usage Guide

### Method 1: Quick Broadcast (Original)
```
/broadcast Hello everyone! This is an announcement.
```

### Method 2: Broadcast with Buttons (New)

**Step 1:** Create your message
```
🎉 Special Announcement!

We've launched new features. Check them out!

| 📢 Channel:t.me/anniemusic | 💬 Support:t.me/support | 🎮 Play:/play
```

**Step 2:** Reply to that message with:
```
/setbroadcast
```

**Step 3:** The bot will show you a preview of your broadcast.

**Step 4:** Start the broadcast:
```
/startbroadcast -pin
```

### Method 3: Image Broadcast (New)

**Step 1:** Send a photo with caption:
```
🎵 New Music Player Update

Enjoy better quality and new features!

| Try Now:t.me/bot?start=help | Support:t.me/support
```

**Step 2:** Reply to the photo with:
```
/setbroadcast
```

**Step 3:** Start the broadcast:
```
/startbroadcast
```

---

## Button Configuration

### Button Format
Buttons are defined using the pipe (`|`) separator:
```
Message Text | Button1:URL1 | Button2:URL2 | Button3:URL3
```

### Button Types
Currently supported: **URL Buttons** (opens links)

### Button Layout
- Buttons are automatically arranged in rows of 2
- Example with 4 buttons:
  ```
  [Button 1] [Button 2]
  [Button 3] [Button 4]
  ```

### Examples

**Example 1: Support Links**
```
Need help? Contact us! | Support Group:t.me/support | Channel:t.me/channel
```

**Example 2: Social Media**
```
Follow us on social media! | YouTube:https://youtube.com | Instagram:https://instagram.com | Twitter:https://twitter.com
```

**Example 3: Bot Commands (as URLs)**
```
Try these commands! | Play Music:t.me/yourbot?start=/play | Help:t.me/yourbot?start=/help
```

---

## Features

### ✅ What's Supported
1. **Text Messages** - Plain text broadcasts
2. **Images** - Photos with captions
3. **Inline Buttons** - URL buttons in inline keyboard format
4. **HTML Formatting** - Use `<b>`, `<i>`, `<code>`, `<a href>`, etc.
5. **Pinning** - Auto-pin messages in chats
6. **Targeted Broadcasting** - Send to chats, users, or both
7. **Assistant Broadcast** - Broadcast via assistant accounts

### 🔄 Broadcasting Stats
After broadcast completes, you'll receive:
- Number of chats/users the message was sent to
- Number of messages successfully pinned
- Error handling for failed deliveries

---

## Important Notes

### ⚠️ Limitations
1. **Rate Limiting** - The bot automatically handles Telegram's rate limits (FloodWait)
2. **Button Limits** - Telegram allows maximum 100 buttons per inline keyboard
3. **URL Only** - Currently only URL buttons are supported (not callback buttons)
4. **HTML Parse Mode** - Messages are sent with HTML parsing enabled

### 💡 Best Practices
1. **Test First** - Test your broadcast in a test group before sending to all users
2. **Keep it Simple** - Don't overload with too many buttons (3-5 is optimal)
3. **Use Images Wisely** - Images should be relevant and optimized (under 5MB)
4. **Pin Responsibly** - Only pin important announcements
5. **Timing** - Broadcast during active hours for better engagement

### 🔒 Permissions Required
- Bot must be admin in target groups to pin messages
- Bot needs "Pin Messages" permission for pinning
- SUDOERS access required to use broadcast commands

---

## Troubleshooting

### Issue: Broadcast not sending
**Solution:** Check if bot is admin in target groups

### Issue: Buttons not showing
**Solution:** Verify button format uses `|` and `:` correctly

### Issue: Image not sending
**Solution:** Ensure image is under 10MB and in supported format (JPG, PNG)

### Issue: Pin failing
**Solution:** Bot needs admin rights with "Pin Messages" permission

---

## Technical Details

### How It Works
1. `/setbroadcast` stores content in `app.BROADCAST_CONTENT`
2. Content includes: text, photo_id, reply_markup (buttons)
3. `/startbroadcast` retrieves stored content and sends to all targets
4. Automatic error handling and rate limit management

### Code Structure
```
broadcast.py
├── /broadcast (original command)
├── /newbroadcast (interactive guide)
├── /setbroadcast (set content)
└── /startbroadcast (execute broadcast)
```

---

## Examples Gallery

### Example 1: Simple Text Broadcast
```
/startbroadcast
```
Content: "Hello everyone! How are you?"

### Example 2: Image + Text + Buttons
```
Photo Caption: "🎉 New Update Available!

✨ Features:
- Better sound quality
- New commands
- Improved performance

| Read More:t.me/channel | Support:t.me/support | Update Now:/update"
```

### Example 3: Announcement with Multiple Links
```
Text: "📢 Join Our Community!

🎵 Music | 🎮 Games | 💬 Chat

| Music Channel:t.me/music | Game Bot:t.me/gamebot | Chat Group:t.me/chat | Instagram:https://instagram.com"
```

---

## Future Enhancements (Planned)
- [ ] Callback buttons (for inline interactions)
- [ ] Button rows customization
- [ ] Scheduled broadcasts
- [ ] Broadcast templates
- [ ] Analytics and tracking
- [ ] Markdown support alongside HTML

---

## Support
For issues or questions about the broadcast feature:
- Open an issue on GitHub
- Contact the support group
- Check the bot's help menu with `/help`

---

**Last Updated:** April 23, 2026
**Version:** 2.0
