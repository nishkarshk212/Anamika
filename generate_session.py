"""
Pyrogram Session String Generator
Run this script to generate a session string for your Telegram account.
"""

from pyrogram import Client
import asyncio

# Your API credentials from .env file
API_ID = 30521437
API_HASH = "9b01f57a7511278377202d843c9bfc34"

async def generate_session():
    print("\n" + "="*60)
    print("  Pyrogram Session String Generator")
    print("="*60 + "\n")
    
    async with Client(
        "session_generator",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    ) as app:
        print("✓ Login successful!")
        session_string = await app.export_session_string()
        
        print("\n" + "="*60)
        print("  YOUR SESSION STRING:")
        print("="*60)
        print(f"\n{session_string}\n")
        print("="*60)
        print("\n⚠️  IMPORTANT: Keep this session string secure!")
        print("   Copy it to your .env file as STRING_SESSION\n")

if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n\n❌ Session generation cancelled.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
