from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from anibot import anibot, LOG_CHANNEL_ID


SPO = """
➡️ **☠️LOG STURO☠️** ⬅️

📛**Triggered Command** : /help 
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @GojoSatoru_Xbot
➕➕➕➕➕➕➕➕➕➕➕➕➕
"""



hlp_cmd = """
__This is a small guide on how to use me
    
**Basic Commands:**
Use /ping or !ping cmd to check if bot is online
Use /start or !start cmd to start bot in group or pm
Use /help or !help cmd to get interactive help on available bot cmds
Use /feedback cmd to contact bot owner__

©️ @XBOTS_X
"""


hlp_bt = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🍃 Additional", callback_data="adl"),
                InlineKeyboardButton("🌀 Anilist", callback_data="anl")
             ],[
                InlineKeyboardButton("👥 Group", callback_data="grp"),
                InlineKeyboardButton("🕵️ Oauth", callback_data="oth")
            ],[
                InlineKeyboardButton("➕ Extras", callback_data="ext")
            ]
        ]
)


@anibot.on_message(filters.private & filters.command("help"))
async def hlp_cmd(bot, message):
    await bot.send_message(LOG_CHANNEL_ID, SPO.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    await message.reply_photo(
        photo="https://telegra.ph/file/6efbdbcb4038e995ac6af.jpg",
        caption=hlp_cmd, 
        reply_markup=hlp_bt,
    )
    await message.delete()

#CALLBACK 1

@anibot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "hlp":
        await update.message.edit_text(
            text=hlp_cmd, #update.from_user.first_name
            reply_markup=hlp_bt,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
#MAINE CM
   
    elif update.data == "adl":
        await update.message.edit_text(
            text=ADL_TEXT,
            reply_markup=ADL_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
        
    elif update.data == "anl":
        await update.message.edit_text(
            text=ANL_TEXT,
            reply_markup=ANL_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif update.data == "grp":
        await update.message.edit_text(
            text=GRP_TEXT,
            reply_markup=GRP_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif update.data == "oth":
        await update.message.edit_text(
            text=OTH_TEXT,
            reply_markup=OTH_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
        
    elif update.data == "ext":
        await update.message.edit_text(
            text=EXT_TEXT,
            reply_markup=EXT_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif update.data == "ext2":
        await update.message.edit_text(
            text=EXT2_TEXT,
            reply_markup=EXT2_BUTTONS,
            disable_web_page_preview=True
        )
        await update.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif update.data == "close":
        await update.message.delete()
        await update.answer("Successfully Closed ❌")

#===============

#Callback 2=========
"""
@anibot.on_callback_query(filters.regex("help_callback"))
async def cb_handler(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    if cb == "hlp":
        await CallbackQuery.edit_message_text(
            text=hlp_cmd, 
            reply_markup=hlp_bt
        )
    elif cb == "adl":
        await CallbackQuery.edit_message_text(
            text=ADL_TEXT, 
            reply_markup=ADL_BUTTONS
        )
    elif cb == "anl":
        await CallbackQuery.edit_message_text(
            text=ANL_TEXT, 
            reply_markup=ANL_BUTTONS
        )
    
"""
#==========≠==


ADL_TEXT = """
__Use /reverse cmd to get reverse search via tracemoepy API
Note: This works best on uncropped anime pic,
when used on cropped media, you may get result but it might not be too reliable

Use /schedule cmd to get scheduled animes based on weekdays

Use /watch cmd to get watch order of searched anime

Use /fillers cmd to get a list of fillers for an anime

Use /quote cmd to get a random quote

Use /studio give a query to search about anime!!!

Use /airing give a query to search about airing

Just type /browse to get anime list

Use /gettags to get Anime #tags__ 

©️ @XBOTS_X
"""
ADL_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

ANL_TEXT = """
__Below is the list of basic anilist cmds for info on anime, character, manga, etc.

/anime - Use this cmd to get info on specific anime using keywords (anime name) or Anilist ID
(Can lookup info on sequels and prequels)

/anilist - Use this cmd to choose between multiple animes with similar names related to searched query
(Doesn't includes buttons for prequel and sequel)

/character - Use this cmd to get info on character

/manga - Use this cmd to get info on manga

/airing - Use this cmd to get info on airing status of anime

/top - Use this cmd to lookup top animes of a genre/tag or from all animes
(To get a list of available tags or genres send /gettags or /getgenres
'/gettags nsfw' for nsfw tags)

/user - Use this cmd to get info on an anilist user

/browse - Use this cmd to get updates about latest animes__

©️ @XBOTS_X
"""
ANL_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

GRP_TEXT = """
__Group based commands:

/settings - Toggle stuff like whether to allow 18+ stuff in group or whether to notify about aired animes, etc and change UI

/disable - Disable use of a cmd in the group (Disable multiple cmds by adding space between them)
/disable anime anilist me user

/enable - Enable use of a cmd in the group (Enable multiple cmds by adding space between them)
/enable anime anilist me user

/disabled - List out disabled cmds__

©️ @XBOTS_X
"""
GRP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

OTH_TEXT = """__
This includes advanced anilist features

Use /auth or !auth cmd to get details on how to authorize your Anilist account with bot
Authorising yourself unlocks advanced features of bot like:
- adding anime/character/manga to favourites
- viewing your anilist data related to anime/manga in your searches which includes score, status, and favourites
- unlock /flex, /me, /activity and /favourites commands
- adding/updating anilist entry like completed or plan to watch/read
- deleting anilist entry

Use /flex or !flex cmd to get your anilist stats

Use /logout or !logout cmd to disconnect your Anilist account

Use /me or !me cmd to get your anilist recent activity
Can also use /activity or !activity

Use /favourites or !favourites cmd to get your anilist favourites__

©️ @XBOTS_X
"""
OTH_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

EXT_TEXT = """
__I have some more Extra commands, you can just try it out.

Use /afk [Reason > Optional] - Tell others that you are AFK (Away From Keyboard).
/afk [reply to media] - AFK with media.
Use /askai Ask questions using ai for responding to user queries feom Gamini.
Use /aii Reply to image to containing text that you want transcripts, and  I'll process the image and provide you with the transcribed text.
Use /aicook Reply to image To get cooking instruction of the food in it.
Use /aiseller Reply to image and create you product desc.
Use /gptai /gpt2 /iri /assis Ask anything to gpt ai.
Use /bard Ask anything to Bard ai.
Use /deep ask questions to Deep Ai.
Use /bing2 search any from Bing browser.
Use /info To get your information.
Use /upscale Upscales your image quality.
Use /tagall to Mention all members in Group, or you can type /stop to mentioning to.__

©️ @XBOTS_X
"""
EXT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close"),
        InlineKeyboardButton("Next ➡️", callback_data="ext2")
        ]]
    ) 

EXT2_TEXT = """
**Extraas 2**
__Use /ranking /today to Check it out your Top ranking.
Use /nightmode To set your group night Mod.
Use /rmbg Reply to image to remove Background.
Use /sangmata_set [on/off] created simple detection to check user data include username, first_name, and last_name sangmata in groups.
Use /tmdb to get Move informations from The Movie Database [[TMDB](https://www.themoviedb.org)]
Use /unpic, /unrand to get images from [Unsplash](https://unsplash.com/)
Use /unzip Reply to Zipped files to separates files from zip.
**Whisper:**
Use `@GojoSatoru_Xbot (Target Username or ID) (Your Message)` In inline to use this on group.
Use /imdb [Movename/Series Name]­ Get information about a Movie/Series­..
Use /googleimg It retrieves and displays images obtained through a Google image search.
Use /google_search To get Google search result with links.
Use /bingimg It retrieves and displays images obtained through a Bing image search.
Use /bingsearch To get Bing search result with links.
Use /news_search To search Latest news.
Use /wikisearch To Search Wikipedia quarys.

©️ @XBOTS_X
"""
EXT2_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="ext"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 
