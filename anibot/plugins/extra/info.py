import os
import asyncio
import pyrogram
from pyrogram import Client, filters
from anibot import anibot as app



import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, Optional

EVAA = [
    [
        InlineKeyboardButton(text="Add me to group", url=f"https://t.me/GojoSatoru_Xbot?startgroup=true"),
    ],
]

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

# --------------------------------------------------------------------------------- #


async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],    
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((534, 534))
        bg.paste(resized, (607, 86), resized)

    img_draw = ImageDraw.Draw(bg)

    

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path
   

# --------------------------------------------------------------------------------- #

bg_path = "assets/IN.PNG"
font_path = "assets/hiroko.ttf"

#
# --------------------------------------------------------------------------------- #


INFO_TEXT = """
ㅤ× User Information ×
×───────────────×
  
× User Id: `{}`
× Username: @{}
× Mention: {}
× Status: `{}`
× Dc Id: {}
× Bio: {}

๏ Powered by: [X Bots](https://t.me/xbots_x)
"""

# --------------------------------------------------------------------------------- #

async def userstatus(user_id):
   try:
      user = await app.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "User was seen recently."
      elif x == enums.UserStatus.LAST_WEEK:
          return "User was seen last week."
      elif x == enums.UserStatus.LONG_AGO:
          return "User was seen long ago."
      elif x == enums.UserStatus.OFFLINE:
          return "User is offline."
      elif x == enums.UserStatus.ONLINE:
         return "User is online."
   except:
        return "**Something went wrong!**"
    

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(["info", "information", "userinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await app.download_media(user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, username, mention, status, dc_id, bio), reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(EVAA),)
        except Exception as e:
            await message.reply_text(str(e))        
      
    elif not message.reply_to_message:
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await app.download_media(user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, username, mention, status, dc_id, bio), reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(EVAA),)
        except Exception as e:
            await message.reply_text(str(e))

            
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await app.download_media(message.reply_to_message.from_user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, username, mention, status, dc_id, bio), reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(EVAA),)
        except Exception as e:
            await message.reply_text(str(e))

####




bullets = {
    "bullet1": ">",
    "bullet2": "•",
    "bullet3": "⋟",
    "bullet4": "◈",
    "bullet5": "┏",
    "bullet6": "┣",
    "bullet7": "┗",
}

b1 = bullets["bullet4"]
b2 = bullets["bullet2"]
b3 = bullets["bullet3"]
b4 = bullets["bullet4"]
b5 = bullets["bullet5"]
b6 = bullets["bullet6"]
b7 = bullets["bullet7"]

dc_id = {
    1: "Miami FL, USA",
    2: "Amsterdam, NL",
    3: "Miami FL, USA",
    4: "Amsterdam, NL",
    5: "Singapore, SG",
}


@Client.on_message(filters.command(["2info", "whois"]))
async def whois(bot, message):
    global chat
    msg = await message.reply_text("`Processing...`")
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif len(message.text.split(" ", 1)) == 1 and not message.reply_to_mssage:
        user = message.from_user.id
        chat = message.chat.id
        t = "Chat id: {}".format(chat)

    elif len(message.text.split(" ", 1)) == 2 and not message.reply_to_message:
        user = message.text.split(" ", 1)[1]
    else:
        return await msg.edit("`Give a username or reply to a user..`")
    try:
        ui = await bot.get_users(user)
    except Exception as e:
        return await msg.edit("`Failed to get user`")
    xio = f"{ui.dc_id} | {dc_id[ui.dc_id]}" if ui.dc_id else "Unknown"
    ui_text = [
        f"  {b3} <b>User-info of <i>{ui.mention}</i> :</b>\n\n",
        f"  {b1} <b>Firstname : <i>{ui.first_name}</i></b>\n",
        f"  {b1} <b>Lastname : <i>{ui.last_name}</i></b>\n" if ui.last_name else "",
        (f"  {b1} <b>Username :</b> <code>@{ui.username}</code>\n" if ui.username else ""),
        f"  {b1} <b>User ID :</b> <code>{ui.id}</code>\n",
        f"  {b2} <b>User DCID : <i>{xio}</i></b>\n",
        f"  {b2} <b>Premium User : <i>{ui.is_premium}</i></b>\n"
        f"  {b2} <b>Status : <i>{ui.status}</i></b>\n",
        f"  {b2} <b>Is Bot : <i>{'Yes' if ui.is_bot else 'No'}</i></b>\n",
        f"  {b2} <b>Is Scam : <i>{'Yes' if ui.is_scam else 'No'}</i></b>\n",
        f"  {b2} <b>Is Mutual : <i>{'Yes' if ui.is_mutual_contact else 'No'}</i></b>\n",
        f"  {b2} <b>Is Verified : <i>{'Yes' if ui.is_verified else 'No'}</i></b> \n",
        f"  {b2} <b>This Chat ID : <i>{message.chat.id}</i></b>\n",
    ]
    pic = ui.photo.big_file_id if ui.photo else None
    if pic is not None:
        await msg.delete()
        photo = await bot.download_media(pic)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption="".join(ui_text),
            reply_to_message_id=message.id,
        )
        if os.path.exists(photo):
            os.remove(photo)
    else:
        await msg.edit("".join(ui_text))

@Client.on_message(filters.command(["chatinfo", "cinfo"]))
async def chat_info(c, m):
    # Check if the command has an argument (chat ID)
    if len(m.command) > 1:
        chat_id = m.command[1]
    else:
        chat_id = m.chat.id
    s = await m.reply_text("`Processing...`")
    try:
        cht = await c.get_chat(chat_id)
        msg = f"**❖ Chat Info** \n\n"
        msg += f"**⦾ Chat Title :** `{cht.title}` \n"
        msg += f"**⦾ Chat-ID :** `{cht.id}` \n"
        msg += f"**⦾ Verified :** `{cht.is_verified}` \n"
        msg += f"**⦾ Is Scam :** `{cht.is_scam}` \n"
        if cht.dc_id:
            msg += f"**⦾ Chat DC :** `{cht.dc_id}` \n"
        if cht.username:
            msg += f"**⦾ Chat Username :** `{cht.username}` \n"
        if cht.description:
            msg += f"**â¦¾ Chat Description :** `{cht.description}` \n"
        msg += f"**⦾ Chat Members Count :** `{cht.members_count}` \n"
        if cht.photo:
            kek = await c.download_media(cht.photo.big_file_id)
            await c.send_photo(m.chat.id, photo=kek, caption=msg)
            await s.delete()
            os.remove(kek)
        else:
            await s.edit(msg)
    except Exception as e:
        await s.edit(f"**An error occurred:** `{str(e)}`")


# Define handlers for different types of messages
@app.on_message(filters.private & filters.video)
async def handle_video(bot, message):
    # Handle video message
    await message.reply_text(f"Video file ID: {message.video.file_id}")

@app.on_message(filters.private & filters.sticker)
async def handle_sticker(bot, message):
    # Handle sticker message
    await message.reply_text(f"Sticker file ID: {message.sticker.file_id}")

@app.on_message(filters.private & filters.photo)
async def handle_photo(bot, message):
    # Handle photo message
    await message.reply_text(f"Photo file ID: {message.photo.file_id}")

@app.on_message(filters.private & filters.document)
async def handle_document(bot, message):
    # Handle document message
    await message.reply_text(f"Document file ID: {message.document.file_id}")

# Define handlers for voice and audio messages
@app.on_message(filters.private & filters.voice)
async def handle_voice(bot, message):
    # Handle voice message
    await message.reply_text(f"Voice file ID: {message.voice.file_id}")

@app.on_message(filters.private & filters.audio)
async def handle_audio(bot, message):
    # Handle audio message
    await message.reply_text(f"Audio file ID: {message.audio.file_id}")
    
