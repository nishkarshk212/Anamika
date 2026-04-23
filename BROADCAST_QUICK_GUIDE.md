# Broadcast Feature - Quick Reference

## 🚀 New Commands Added

### 1️⃣ `/newbroadcast`
Shows instructions on how to use the enhanced broadcast feature.

### 2️⃣ `/setbroadcast` 
**Reply to a message** with this command to set it as broadcast content.

**Supported:**
- ✅ Text messages
- ✅ Photos/Images with captions
- ✅ Inline buttons (URL buttons)

### 3️⃣ `/startbroadcast`
Starts the broadcast with the content you set.

**Flags:**
- `-pin` → Pin message (silent)
- `-pinloud` → Pin message (with notification)
- `-user` → Send to users only
- `-nobot` → Don't send to bots

---

## 📝 Button Format

Use the pipe `|` symbol to separate text and buttons:

```
Your message text | Button1:URL1 | Button2:URL2
```

### Examples:

**Example 1: Simple buttons**
```
📢 Join our channels! | Support:t.me/support | Channel:t.me/channel
```

**Example 2: Image with buttons**
Send a photo with caption:
```
🎉 New feature available! | Try Now:t.me/bot?start=help | Help:t.me/support
```
Then reply with `/setbroadcast`

**Example 3: Multiple buttons**
```
Follow us! | YouTube:https://youtube.com | Instagram:https://instagram.com | Twitter:https://twitter.com | Facebook:https://facebook.com
```
Buttons will be arranged in rows of 2 automatically.

---

## 🎯 Usage Flow

### Method 1: Quick Text Broadcast
```
/broadcast Hello everyone!
```

### Method 2: Broadcast with Buttons (NEW)
```
Step 1: Send message → "Announcement | Button1:URL1 | Button2:URL2"
Step 2: Reply to it → /setbroadcast
Step 3: Start broadcast → /startbroadcast
```

### Method 3: Image Broadcast (NEW)
```
Step 1: Send photo with caption → "Text | Button:URL"
Step 2: Reply to photo → /setbroadcast
Step 3: Start broadcast → /startbroadcast -pin
```

---

## 📊 What Gets Sent

The broadcast will be sent with:
- ✅ Your text (HTML formatting supported)
- ✅ Your image (if provided)
- ✅ Inline buttons (if configured)
- ✅ Proper formatting and layout

---

## ⚡ Quick Examples

### Text Only
```
/startbroadcast
```

### With Pin
```
/startbroadcast -pin
```

### To Users Only
```
/startbroadcast -user
```

### Pin with Notification
```
/startbroadcast -pinloud
```

---

## 🔧 Technical Notes

- **Parse Mode:** HTML
- **Button Layout:** 2 buttons per row
- **Rate Limits:** Auto-handled
- **Error Handling:** Built-in
- **Storage:** Temporary (cleared after broadcast)

---

## ⚠️ Requirements

- Must be SUDOER to use these commands
- Bot needs admin rights to pin messages
- "Pin Messages" permission required for pinning

---

## 📖 Full Documentation

See `BROADCAST_FEATURES.md` for complete documentation.
