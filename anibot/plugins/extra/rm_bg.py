import asyncio

import os

import time 
import json 

import random
import string
import requests

from pyrogram import enums
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto

import aiohttp
import aiofiles

from anibot import anibot as app

from anibot.utils2.helper.api import getFile, UpscaleImages
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram.enums import ChatAction, ParseMode





#°==
def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid

async def RemoveBG(input_file_name):
    headers = {"X-API-Key": "w7zXrXXmmYgGjCvc7BrHeqfz"}
    files = {"image_file": open(input_file_name, "rb").read()}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            "https://api.remove.bg/v1.0/removebg", headers=headers, data=files
        ) as y:
            contentType = y.headers.get("content-type")
            if "image" not in contentType:
                return False, (await y.json())

            name = check_filename("alpha.png")
            file = await aiofiles.open(name, "wb")
            await file.write(await y.read())
            await file.close()
            return True, name
bgr = InlineKeyboardMarkup(
               [
                   [
                      InlineKeyboardButton('My Group', url='https://t.me/songdownload_group')
                   ]
               ]
         )
@app.on_message(filters.command("rmbg", CMD) & pyro_cooldown.wait(10))
async def rmbg(bot, message):
  rmbg = await message.reply("__Processing your image...__") 
  replied = message.reply_to_message
  if not replied:
      return await rmbg.edit("Reply to a photo to Remove it's Backgroud")

  if replied.photo:
      photo = await bot.download_media(replied)
      x, y = await RemoveBG(photo)
      os.remove(photo)
      if not x:
          bruh = y["errors"][0]
          details = bruh.get("detail", "")
          return await rmbg.edit(f"ERROR ~ {bruh['title']},\n{details}")
      await message.reply_photo(photo=y, caption="Here is your Image without Background", reply_markup=bgr)
      await message.reply_document(document=y)
      await rmbg.delete()
      return os.remove(y)
  await rmbg.edit("Reply only to a photo to Remove it's Background")
#===8


@app.on_message(filters.command("upscale", CMD) & pyro_cooldown.wait(10))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("__Replay to an image.__")
    msg = await message.reply("__wait a minutes...__")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"))
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}")
