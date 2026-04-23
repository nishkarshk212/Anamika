# Broadcast Feature Workflow

## 📋 Command Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    BROADCAST COMMANDS                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  /broadcast      │ ────► Original command (text only)
│  (original)      │      Supports: -pin, -user, -assistant
└──────────────────┘

┌──────────────────┐
│ /newbroadcast    │ ────► Shows setup instructions
│  (new)           │      Guides user on formatting
└──────────────────┘

┌──────────────────┐
│ /setbroadcast    │ ────► Sets broadcast content
│  (new)           │      Stores: text, image, buttons
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│              CONTENT PARSING PROCESS                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  1. Extract text from message/caption                     │
│  2. Check for photo → store photo_id                      │
│  3. Parse buttons from text (if "|" present)              │
│  4. Create InlineKeyboardMarkup                           │
│  5. Store in app.BROADCAST_CONTENT                        │
│                                                           │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────┐
│ /startbroadcast  │ ────► Executes broadcast
│  (new)           │      Sends to all users/chats
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│              BROADCAST EXECUTION                          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────┐             │
│  │  For each chat in served_chats:         │             │
│  │  ├─ Send text OR photo                  │             │
│  │  ├─ Attach inline buttons (if any)      │             │
│  │  ├─ Pin message (if -pin flag)          │             │
│  │  └─ Track success/failure               │             │
│  └─────────────────────────────────────────┘             │
│                                                           │
│  ┌─────────────────────────────────────────┐             │
│  │  If -user flag:                         │             │
│  │  ├─ For each user in served_users       │             │
│  │  ├─ Send text OR photo                  │             │
│  │  ├─ Attach inline buttons (if any)      │             │
│  │  └─ Track success/failure               │             │
│  └─────────────────────────────────────────┘             │
│                                                           │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    COMPLETION                             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ✅ Broadcast completed!                                  │
│  📊 Stats:                                                │
│    • Sent to X chats                                      │
│    • Pinned in Y chats                                    │
│    • Sent to Z users (if -user flag)                      │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Content Parsing Flow

```
User sends message:
"📢 Announcement! | Support:t.me/support | Channel:t.me/channel"
         │
         ▼
┌─────────────────────────────────────┐
│         TEXT PARSING                │
├─────────────────────────────────────┤
│                                      │
│  Split by "|":                      │
│  ├─ Part 0: "📢 Announcement!"      │
│  │   → This is the main text        │
│  │                                   │
│  ├─ Part 1: "Support:t.me/support"  │
│  │   → Split by ":"                 │
│  │   → Button: "Support"            │
│  │   → URL: "t.me/support"          │
│  │                                   │
│  └─ Part 2: "Channel:t.me/channel"  │
│      → Split by ":"                 │
│      → Button: "Channel"            │
│      → URL: "t.me/channel"          │
│                                      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│      BUTTON LAYOUT CREATION         │
├─────────────────────────────────────┤
│                                      │
│  Original buttons:                  │
│  [Support] [Channel]                │
│                                      │
│  Arranged in rows of 2:             │
│  ┌──────────────────────┐           │
│  │ [Support] [Channel]  │           │
│  └──────────────────────┘           │
│                                      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│       FINAL MESSAGE STRUCTURE       │
├─────────────────────────────────────┤
│                                      │
│  📢 Announcement!                    │
│                                      │
│  ┌──────────────────────┐           │
│  │ [Support] [Channel]  │           │
│  └──────────────────────┘           │
│                                      │
└─────────────────────────────────────┘
```

---

## 📊 Broadcast Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│                  START BROADCAST                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 1: Check flags                                    │
│  ├─ -pin / -pinloud → Enable pinning                    │
│  ├─ -user → Include user broadcast                      │
│  └─ -nobot → Skip bot chats                             │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: Broadcast to chats                             │
│  ├─ Get all served_chats from database                  │
│  ├─ For each chat:                                      │
│  │  ├─ Check if content has photo                       │
│  │  │  ├─ YES → send_photo() with caption + buttons     │
│  │  │  └─ NO → send_message() with text + buttons       │
│  │  ├─ If pin flag enabled:                             │
│  │  │  └─ pin message in chat                           │
│  │  ├─ Increment success counter                        │
│  │  └─ Sleep 0.2s (rate limiting)                       │
│  └─ Handle FloodWait errors automatically               │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: Broadcast to users (if -user flag)             │
│  ├─ Get all served_users from database                  │
│  ├─ For each user:                                      │
│  │  ├─ Check if content has photo                       │
│  │  │  ├─ YES → send_photo() with caption + buttons     │
│  │  │  └─ NO → send_message() with text + buttons       │
│  │  ├─ Increment success counter                        │
│  │  └─ Sleep 0.2s (rate limiting)                       │
│  └─ Handle FloodWait errors automatically               │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: Completion                                     │
│  ├─ Set IS_BROADCASTING = False                         │
│  ├─ Clear app.BROADCAST_CONTENT                         │
│  └─ Send completion stats to admin                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Example Scenarios

### Scenario 1: Simple Text Broadcast
```
Admin: /broadcast Hello everyone!

Flow:
/broadcast → Parse text → Send to all chats → Done
```

### Scenario 2: Broadcast with Buttons
```
Admin: "📢 Join us! | Support:t.me/support | Channel:t.me/channel"
Admin: /setbroadcast (replying to above)
Admin: /startbroadcast

Flow:
/setbroadcast → Parse text & buttons → Store content
/startbroadcast → Retrieve content → Send with buttons → Done
```

### Scenario 3: Image Broadcast with Pin
```
Admin: [Sends photo with caption]
       "🎉 Update! | Try:t.me/bot?start=help"
Admin: /setbroadcast (replying to photo)
Admin: /startbroadcast -pin

Flow:
/setbroadcast → Extract photo_id & text → Parse buttons → Store
/startbroadcast → Send photo + caption + buttons → Pin → Done
```

---

## ⚙️ Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATABASE                              │
│                                                          │
│  served_chats  →  [chat_id: 123, chat_id: 456, ...]    │
│  served_users  →  [user_id: 789, user_id: 012, ...]    │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  BROADCAST MODULE                        │
│                                                          │
│  app.BROADCAST_CONTENT (temporary storage):             │
│  {                                                       │
│    "text": "Your message",                              │
│    "photo_id": "AgACAgQAAx...", (optional)              │
│    "reply_markup": InlineKeyboardMarkup, (optional)     │
│    "message_id": 12345,                                 │
│    "chat_id": 67890                                     │
│  }                                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               PYROGRAM API CALLS                         │
│                                                          │
│  • app.send_message(chat_id, text, reply_markup)        │
│  • app.send_photo(chat_id, photo, caption, reply_markup)│
│  • message.pin(disable_notification=True/False)         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Security & Permissions

```
┌─────────────────────────────────────────────────────────┐
│              PERMISSION CHECKS                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. Command Execution:                                  │
│     └─ Must be in SUDOERS list                          │
│                                                           │
│  2. Pinning Messages:                                   │
│     ├─ Bot must be admin in chat                        │
│     └─ Must have "Pin Messages" permission              │
│                                                           │
│  3. Broadcasting:                                       │
│     ├─ Bot must be member of target chat                │
│     └─ Must have "Send Messages" permission             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Rate Limiting & Error Handling

```
┌─────────────────────────────────────────────────────────┐
│              FLOOD CONTROL                               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Between each message:                                  │
│  └─ asyncio.sleep(0.2)  # 200ms delay                   │
│                                                           │
│  On FloodWait error:                                    │
│  ├─ Catch FloodWait exception                           │
│  ├─ If wait time > 200s → Skip                          │
│  └─ If wait time <= 200s → Wait and continue            │
│                                                           │
│  On other errors:                                       │
│  └─ Continue to next chat/user (don't stop)             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Button Layout Examples

### 2 Buttons:
```
┌─────────────────────────────┐
│  [Support]    [Channel]     │
└─────────────────────────────┘
```

### 4 Buttons:
```
┌─────────────────────────────┐
│  [YouTube]   [Instagram]    │
│  [Twitter]   [Facebook]     │
└─────────────────────────────┘
```

### 5 Buttons:
```
┌─────────────────────────────┐
│  [Web]      [Support]       │
│  [Channel]  [GitHub]        │
│  [Donate]                   │
└─────────────────────────────┘
```

---

**Created:** April 23, 2026  
**Version:** 2.0
