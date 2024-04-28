from pyrogram import Client, filters
from pyrogram.types import Message
from anibot import anibot as app
from anibot import OWNER as OWNER_ID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# vc on
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("**⌾ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ ⌾**")

# vc off
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("**⌾ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ ⌾**")

# invite members on vc
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"{message.from_user.mention}\n\n**Inviting vc to**\n\n**➠ **"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        invite_link = await app.export_chat_invite_link(message.chat.id)
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"

        await message.reply(reply_text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text= "✙ ᴧᴅᴅ ᴍᴇ ✙", url=add_link)],
        ]))
    except Exception as e:
        print(f"Error: {e}")


####
