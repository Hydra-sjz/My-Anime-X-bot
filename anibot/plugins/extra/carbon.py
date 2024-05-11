import aiohttp
from io import BytesIO
from anibot import anibot as app
from pyrogram import filters



async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image



@app.on_message(filters.command("carbon"))
async def _carbon(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("**𝘙𝘦𝘱𝘭𝘺 𝘵𝘰 𝘢 𝘵𝘦𝘹𝘵 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘵𝘰 𝘮𝘢𝘬𝘦 𝘢 𝘤𝘢𝘳𝘣𝘰𝘯.**")
        return
    if not (replied.text or replied.caption):
        return await message.reply_text("**𝘙𝘦𝘱𝘭𝘺 𝘵𝘰 𝘢 𝘵𝘦𝘹𝘵 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘵𝘰 𝘮𝘢𝘬𝘦 𝘢 𝘤𝘢𝘳𝘣𝘰𝘯.**")
    text = await message.reply("Processing...")
    carbon = await make_carbon(replied.text or replied.caption)
    await text.edit("**𝘜𝘱𝘭𝘰𝘢𝘥𝘪𝘯𝘨...**")
    await message.reply_photo(carbon)
    await text.delete()
    carbon.close()
