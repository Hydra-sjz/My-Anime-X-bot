import requests

import random
from anibot import anibot
from pyrogram import filters
from pyrogram import enums



@anibot.on_message(filters.private & filters.command("boobs"))
async def boobs(_, message):
    file_id = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    url = "http://media.oboobs.ru/{}"
    await anibot.send_photo(message.chat.id, url.format(file_id),protect_content=True, reply_to_message_id=message.id)




     
