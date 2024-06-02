from anibot import anibot as app
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.types import InlineQuery, CallbackQuery
    
from anibot.data import *

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("💌 Start Whisper", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []
    
    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="💌 Whisper",
                description="@GojoSatoru_Xbot [ USERNAME | ID ] [ TEXT ]",
                input_message_content=InputTextMessageContent(f"💌 Usage:\n\n@GojoSatoru_Xbot [ USERNAME | ID ] [ TEXT ]"),
                thumb_url="https://telegra.ph/file/10e0f3296a52580094bac.jpg",
                reply_markup=switch_btn
            )
        ]
        
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
        except IndexError as e:
            pass
        
        try:
            user = await _.get_users(user_id)
        except:
            mm = [
                InlineQueryResultArticle(
                    title="💒 Whisper",
                    description="Invalid username or ID!",
                    input_message_content=InputTextMessageContent("❌ Invalid username or ID!"),
                    thumb_url="https://telegra.ph/file/10e0f3296a52580094bac.jpg",
                    reply_markup=switch_btn
                )
            ]
        
        try:
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔩 One-Time Whisper", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="💌 Whisper",
                    description=f"Send a Whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"💌 You are sending a whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://telegra.ph/file/10e0f3296a52580094bac.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="🔩 One-Time Whisper",
                    description=f"Send a one-time whisper to {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"🔩 You are sending a one-time whisper to {user.first_name}.\n\nType your message/sentence."),
                    thumb_url="https://telegra.ph/file/10e0f3296a52580094bac.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
        except:
            pass
        
        try:
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            pass
    
    results.append(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id
    
    if user_id not in [from_user, to_user, 6691393517]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your whisper.")
        except Unauthorized:
            pass
        
        return await query.answer("This whisper is not for you 🚧", show_alert=True)
    
    search_msg = f"{from_user}_{to_user}"
    
    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 Error!\n\nWhisper has been deleted from the database!"
    
    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])
    
    await query.answer(msg, show_alert=True)
    
    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("📬 Whisper has been read!\n\nPress the button below to send a whisper!", reply_markup=SWITCH)



async def in_help(_, inline_query):
    answers = [
        InlineQueryResultArticle(
            title="💌 Whisper",
            description=f"@GojoSatoru_Xbot [USERNAME | ID] [TEXT]",
            input_message_content=InputTextMessageContent(f"**📍Usage:**\n\n@GojoSatoru_Xbot (Target Username or ID) (Your Message).\n\n**Example:**\n@GojoSatoru_Xbot @username I Wanna Phuck You"),
            thumb_url="https://telegra.ph/file/10e0f3296a52580094bac.jpg",
            reply_markup=switch_btn
        ),
        InlineQueryResultArticle(
                title="🎮 Tic-Tac-Toe",
                description="Tap here to challenge your friends in XO!",
                input_message_content=InputTextMessageContent(
                    f"**{inline_query.from_user.first_name}** challenged you in XO!"
                ),
                thumb_url="https://telegra.ph/file/a64892c281f1fa45e2af9.jpg",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        emojis.swords + " Accept",
                        json.dumps(
                            {"type": "P",
                             "id": inline_query.from_user.id,
                             "name": inline_query.from_user.first_name
                            }
                        )
                    )]]
                )
            )
      ]
    return answers


@app.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()
    
    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers[-1], cache_time=0)
                                               
