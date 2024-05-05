
import os

from pyrogram import filters
from pyrogram.types import Message
from telegraph.aio import Telegraph

from anibot import anibot as app, CMD


from httpx import AsyncClient, Timeout
from aiohttp import ClientSession

# Aiohttp Async Client
session = ClientSession()

# HTTPx Async Client
fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)



@app.on_message(filters.command(["ocr"], CMD))
async def ocr(bot, ctx):
    reply = ctx.reply_to_message
    if (
        not reply
        or not reply.sticker
        and not reply.photo
        and (not reply.document or not reply.document.mime_type.startswith("image"))
    ):
        return await ctx.reply_text(
            "Reply photo with /ocr command to scan text from images.", quote=True
        )
    msg = await ctx.reply_text("Scanning your images..", quote=True)
    try:
        file_path = await reply.download()
        if reply.sticker:
            file_path = await reply.download(
                f"ocr_{ctx.from_user.id if ctx.from_user else ctx.sender_chat.id}.jpg"
            )
        response = await Telegraph().upload_file(file_path)
        url = f"https://img.yasirweb.eu.org{response[0]['src']}"
        req = (
            await fetch.get(
                f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}",
                follow_redirects=True,
            )
        ).json()
        await msg.edit(f"**OCR:**\n<code>{}</code>".format(result=req["text"]))
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await msg.edit_msg(str(e))
        if os.path.exists(file_path):
            os.remove(file_path)
