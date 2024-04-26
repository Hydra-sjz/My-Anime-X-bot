# credits to @NotThatMF on telegram for chiaki fast api
# well i also borrowed the base code from him

from pyrogram import filters, Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from .. import BOT_NAME, TRIGGERS as trg, anibot
from ..utils.data_parser import get_wo, get_wols
from ..utils.helper import (
    check_user,
    control_user,
    get_user_from_channel as gcc
)
from ..utils.db import get_collection

DC = get_collection('DISABLED_CMDS')


@anibot.on_message(
    filters.command(["watch", f"watch{BOT_NAME}"], prefixes=trg)
)
@control_user
async def get_watch_order(client: Client, message: Message, mdata: dict):
    """__📜Get List of Scheduled Anime📜__"""
    gid = mdata['chat']['id']
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'watch' in find_gc['cmd_list'].split():
        return
    x = message.text.split(" ", 1)
    if len(x)==1:
        await message.reply_text("😕 __Nothing given to search for!!!__")
        return
    try:
        user = mdata['from_user']['id']
    except KeyError:
        user = mdata['sender_chat']['id']
    data = get_wols(x[1])
    msg = f"__🍃 Found related animes for the query {x[1]}__\n\n©️ @XBOTS_X"
    buttons = []
    if data == []:
        await client.send_message(gid, '❌ No results found!!!')
        return
    for i in data:
        buttons.append(
            [
                InlineKeyboardButton(
                    str(i[1]),
                    callback_data=f"watch_{i[0]}_{x[1]}_0_{user}"
                )
            ]
        )
    await client.send_message(
        gid, msg, reply_markup=InlineKeyboardMarkup(buttons)
    )


@anibot.on_callback_query(filters.regex(pattern=r"watch_(.*)"))
@check_user
async def watch_(client: anibot, cq: CallbackQuery, cdata: dict):
    kek, id_, qry, req, user = cdata['data'].split("_")
    msg, total = get_wo(int(id_), int(req))
    totalpg, lol = divmod(total, 50)
    button = []
    if lol!=0:
        totalpg + 1
    if total>50:
        if int(req)==0:
            button.append(
                [
                    InlineKeyboardButton(
                        text="Next ➡️",
                        callback_data=f"{kek}_{id_}_{qry}_{int(req)+1}_{user}"
                    )
                ]
            )
        elif int(req)==totalpg:
            button.append(
                [
                    InlineKeyboardButton(
                        text="⬅️ Prev",
                        callback_data=f"{kek}_{id_}_{qry}_{int(req)-1}_{user}"
                    )
                ]
            )
        else:
            button.append(
                [
                    InlineKeyboardButton(
                        text="⬅️ Prev",
                        callback_data=f"{kek}_{id_}_{qry}_{int(req)-1}_{user}"
                    ),
                    InlineKeyboardButton(
                        text="Next ➡️",
                        callback_data=f"{kek}_{id_}_{qry}_{int(req)+1}_{user}"
                    )
                ]
            )
    button.append([
        InlineKeyboardButton("◀️ Back", callback_data=f"wol_{qry}_{user}")
    ])
    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(button))


@anibot.on_callback_query(filters.regex(pattern=r"wol_(.*)"))
@check_user
async def wls(client: anibot, cq: CallbackQuery, cdata: dict):
    kek, qry, user = cdata['data'].split("_")
    data = get_wols(qry)
    msg = f"🍃 __Found related animes for the query {qry}__\n\n©️ @XBOTS_X"
    buttons = []
    for i in data:
        buttons.append(
            [
                InlineKeyboardButton(
                    str(i[1]),
                    callback_data=f"watch_{i[0]}_{qry}_0_{user}"
                )
            ]
        )
    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


@anibot.on_edited_message(
    filters.command(["📺 Watch", f"watch{BOT_NAME}"], prefixes=trg)
)
async def get_watch_order_edit(client: Client, message: Message):
    await get_watch_order(client, message)
