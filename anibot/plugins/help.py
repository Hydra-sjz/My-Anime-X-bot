from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from anibot import anibot

hlp_cmd = """
__Hey {} user this is a small guide on how to use me
    
**Basic Commands:**
Use /ping or !ping cmd to check if bot is online
Use /start or !start cmd to start bot in group or pm
Use /help or !help cmd to get interactive help on available bot cmds
Use /feedback cmd to contact bot owner__

©️ @XBOTS_X
"""
startbt = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Additional', callback_data="adl"),
                InlineKeyboardButton('Anilist', callback_data="anl")
            ],[
                InlineKeyboardButton("Group", callback_data="grp"),
                InlineKeyboardButton('Oauth', callback_data="oth")
            ],[
                InlineKeyboardButton('❌', callback_data="")
            ]
        ]
)

@anibot.on_message(filters.private & filters.command("help"))
async def hlp_cmd(bot, message):
    await message.reply_text(
        text=hlp_cmd.format(message.from_user.first_name), 
        reply_markup=hlpbt,
    )
    await message.delete()

@anibot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "hlp":
        await update.message.edit_text(
            text=hlp_cmd.format(update.from_user.first_name), #update.from_user.first_name
            reply_markup=startbt,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif update.data == "cmds":
        await update.message.edit_text(
            text=CMDS_TEXT,
            reply_markup=CMDS_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
