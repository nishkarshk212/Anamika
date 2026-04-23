# Authored By Certified Coders © 2025
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from config import *
from AnnieXMedia import app
from AnnieXMedia.core.call import StreamController
from AnnieXMedia.utils import bot_sys_stats
from AnnieXMedia.utils.decorators.language import language
from AnnieXMedia.utils.inline import supp_markup
from config import BANNED_USERS, OWNER_USERNAME


@app.on_message(filters.command("ping", prefixes=["/", "."]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply(
        _["ping_1"].format(app.mention),
    )
    pytgping = await StreamController.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    owner_mention = f"@{OWNER_USERNAME}" if OWNER_USERNAME else "Unknown"
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping, owner_mention),
        reply_markup=supp_markup(_),
    )
