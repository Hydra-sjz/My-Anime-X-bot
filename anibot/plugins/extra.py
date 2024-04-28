import asyncio
from pyrogram import filters, emoji
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from anibot import anibot as Mbot
import random
import time
import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')

PICS = (
    "https://telegra.ph/file/9ddc4855745329dab4bd2.jpg",
    "https://telegra.ph/file/329550f7ab607e196b58b.jpg",
    "https://telegra.ph/file/8001bbd84321fbe5e5bc1.jpg",
    "https://telegra.ph/file/7dd40f4bf195cf0b9eb4d.jpg",
    "https://telegra.ph/file/f26f465e80e2f92dc8ab0.jpg",
    "https://telegra.ph/file/c91766dd6f09dba41917e.jpg",
    "https://telegra.ph/file/80fc38661b643773a788a.jpg",
    "https://telegra.ph/file/cd65c1461419950f09046.jpg",
    "https://telegra.ph/file/2a0aaf43f957dbe464c7f.jpg",
    "https://telegra.ph/file/2aadb910cfabd588e6a22.jpg",
    "https://telegra.ph/file/4113993db87df2eb7c022.jpg",
    "https://telegra.ph/file/fa206594e9211b1c784f6.jpg"
)


wlc_text = """ 
__Hey there {} Welcome to my ๛ {} Group🎵__

× Name: {}
× User name: @{}
× User ID: `{}`

 ๛ {} Your are here {}Th member of the group!
Joined On:
{}

[Read Rules!!](http://t.me/Hydra_Maneger_bot?start=regole_-1001671054664)
"""

bye_text = """
Nice knowing you.
"""

cap = """
Thanks for joining my Music Galaxy group.🤗❤️
just /start 😜🫰🏼
"""
markup1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="My group", url="https://t.me/songdownload_group"
             ),
        ]
    ]
)

markup2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Group Rules!!", url="http://t.me/Hydra_Maneger_bot?start=regole_-1001671054664"
             ),
        ]
    ]
)
@Mbot.on_message(filters.new_chat_members)
async def welcome(bot, message: Message):
    count = await bot.get_chat_members_count(message.chat.id)
    datetime_ist = datetime.now(IST)
    joined_date = datetime_ist.strftime("`%I:%M %p` | (%d/%B/%Y)")
    ab = await message.reply_photo(
        photo=random.choice(PICS),
        caption=wlc_text.format(message.from_user.mention, message.chat.title, message.from_user.first_name, message.from_user.username, message.from_user.id, message.from_user.first_name, count, joined_date),
        reply_markup=markup2,
    )
    ac = await message.reply_sticker(
        sticker="CAACAgIAAxkBAAIIFmUbGqjPT3l16ow9LKVV5YC-t1xXAAKxIgACzbmQSGxILy9tRT3rHgQ"             
    )
    await bot.send_message(
        message.from_user.id,
        f"{cap}",
        disable_web_page_preview=True,
        reply_markup=markup1,
    )
    await asyncio.sleep(1000)
    await ab.delete()
    await ac.delete()

@Mbot.on_message(filters.left_chat_member)
async def user_left(bot, message: Message):
    ac = await message.reply_text(bye_text)
    await asyncio.sleep(1000)
    await ac.delete()
