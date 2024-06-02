from anibot import anibot as app
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.types import InlineQuery, CallbackQuery
    
from anibot.data import *






switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💌 Start Whisper", switch_inline_query_current_chat="")]])

switch_btn2 = InlineKeyboardMarkup([[InlineKeyboardButton("Accept", switch_inline_query_current_chat="")]])



@app.on_inline_query()
async def inline_t(client: Client, query: InlineQuery):
    string_given = query.query.strip()
    q = string_given.lower()
    if q == "":
        answer = [
            InlineQueryResultArticle(
                title="💌 Whisper",
                description="🍃 @GojoSatoru_Xbot [USERNAME | ID] [TEXT].",
                thumb_url="https://telegra.ph/file/337cb9b64bb3c7462541e.jpg",
                input_message_content=InputTextMessageContent("**📍Usage:**\n\n@GojoSatoru_Xbot (Target Username or ID) (Your Message).\n\n**Example:**\n@GojoSatoru_Xbot @username I Wanna Phuck You."),
                reply_markup=InlineKeyboardMarkup(switch_btn)
            ),
            InlineQueryResultArticle(
                title="❌Tic-Tac-Toe⭕",
                description="Tap here to challenge your friends in XO!",
                thumb_url="https://telegra.ph/file/a64892c281f1fa45e2af9.jpg",
                input_message_content=InputTextMessageContent(f"**{query.from_user.first_name}** challenged you in XO!"),
                reply_markup=InlineKeyboardMarkup(switch_btn2)
            )
        ]
        await query.answer(results=answer, cache_time=5, switch_pm_text="💫 Welcome To @Musicx_dlbot", switch_pm_parameter="help")
