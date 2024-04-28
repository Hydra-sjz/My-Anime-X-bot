from pyrogram.types import Message
from pyrogram import filters
from anibot import anibot as app
from anibot.plugins.anidex.AnimeDex import AnimeDex
from anibot.plugins.anidex.button import BTN
from anibot.plugins.anidex.stats import day, over




@app.on_message(filters.command(['anidex']))
async def searcdhCMD(_, message: Message):
    try:
        user = message.from_user.id
        query = ' '.join(message.command[1:])
        if query == '':
            return await message.reply_text('Give me something to search ^_^')
        data = AnimeDex.search(query)
        button = BTN.searchCMD(user, data, query)
        await message.reply_text(f"**Search Results:** `{query}`", reply_markup=button)
    except Exception as e:
        try:
            return await message.reply_text('**Anime Not Found...**\n\nProbably Incorrect Name, Try again')
        except:
            return





@app.on_message(filters.command('stats1'))
async def stats1(_, message: Message):
    try:
        img = day()
        await message.reply_photo(img, caption='**AnimeDex | Day Wise Stats**')
    except:
        return


@app.on_message(filters.command('stats2'))
async def stats2(_, message: Message):
    try:
        img = over()
        await message.reply_photo(img, caption='**AnimeDex | Overall Stats**')
    except:
        return
