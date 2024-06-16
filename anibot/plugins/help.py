import os
import asyncio
import traceback
import logging

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, CallbackQuery

from anibot import anibot, LOG_CHANNEL_ID
import wget
import requests as re
from pyrogram import *

from anibot.utils2.broadcast_db.broadcast import broadcast
from anibot.utils2.broadcast_db.check_user import handle_user_status
from anibot.utils2.broadcast_db.database import Database
from config import AUTH_USERS, DB_URL, DB_NAME

#from anibot.data import *

db = Database(DB_URL, DB_NAME)

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

buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('Generate', callback_data='generate'),
            InlineKeyboardButton('Refresh', callback_data='refresh'),
            InlineKeyboardButton('Close', callback_data='close')
                   ] 
                             ])

msg_buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('View message', callback_data='view_msg'),
            InlineKeyboardButton('Close', callback_data='close')
                   ] 
                             ])




hlp_cmd = """
```__This is a small guide on how to use me
    
**Basic Commands:**
Use /ping or !ping cmd to check if bot is online
Use /start or !start cmd to start bot in group or pm
Use /help or !help cmd to get interactive help on available bot cmds
Use /feedback cmd to contact bot owner__

©️ @XBOTS_X```
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
                InlineKeyboardButton("👮Mod-CMDS", callback_data="mod"),
                InlineKeyboardButton("➕ Extras", callback_data="ext")
            ]
        ]
)

txt = """
__Owners / Sudos can also use

- __/term__ `to run a cmd in terminal`
- __/eval__ `to run a python code like `__/eval print('UwU')__` `
- __/stats__ `to get stats on bot like no. of users, grps and authorised users`
- __/dbcleanup__ `to remove obsolete/useless entries in database`

Apart from above shown cmds__

©️ @XBOTS_X
"""

start_cmd = """
Hello {} Welcome to Gojo Satoru 𝕏 Bot
"""
startbt = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('📣 My Channel', url='https://t.me/XBots_X')
            ],[
                InlineKeyboardButton("Only for Owner", callback_data="own")
            ]
        ]
)



@anibot.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)
@anibot.on_message(filters.private & filters.command("skw"))
async def starwkommand(bot, message):
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"🥳NEWUSER🥳 \n\n😼New User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) 😹started @spotifysavetgbot !!",
            )
        else:
            logging.info(f"🥳NewUser🥳 :- 😼Name : {message.from_user.first_name} 😹ID : {message.from_user.id}")
    await message.reply_text(
        text=start_cmd.format(message.from_user.first_name), 
        reply_markup=startbt,
    )
    await message.delete()

@anibot.on_message(filters.private & filters.command("help"))
async def hlp_cmd(bot, message):
    await bot.send_message(LOG_CHANNEL_ID, SPO.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    await message.reply_photo(
        photo="https://telegra.ph/file/f04e33ed9774304630ab7.jpg",
        caption=hlp_cmd, 
        reply_markup=hlp_bt,
    )
    await message.reply_text(txt)
    await message.delete()

#CALLBACK 1
email=''
@anibot.on_callback_query()
async def cb_handler(bot, query):
    response=query.data
    if query.data == "hlp":
        await query.message.edit_text(
            text=hlp_cmd, #update.from_user.first_name
            reply_markup=hlp_bt,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif response=='generate':
       global email
       email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
       await query.edit_message_text('__**Your Temporary E-mail: **__`'+str(email)+'`',
                                       reply_markup=buttons)
       print(email)

    elif response=='refresh':
        print(email)
        try:
            if email=='':
                await query.edit_message_text('Genaerate a email',reply_markup=buttons)
            else: 
                getmsg_endp =  "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum=str(ref_response[0]['id'])
                from_msg=ref_response[0]['from']
                subject=ref_response[0]['subject']
                refreshrply='You a message from '+from_msg+'\n\nSubject : '+subject
                await query.edit_message_text(refreshrply,
                                                reply_markup=msg_buttons)
        except:
            await query.answer('No messages were received..\nin your Mailbox '+email)
    elif response=='view_msg':
        msg =re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail=msg['from']
        date=msg['date']
        subjectt=msg['subject']
        try:
          attachments=msg['attachments'][0]
        except:
            pass
        body=msg['body']
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        await update.edit_message_text(mailbox_view,reply_markup=buttons)
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        if attachments == "[]":
            await query.edit_message_text(mailbox_view,reply_markup=buttons)
            await query.answer("No Messages Were Recieved..", show_alert=True)
        else:
            dlattach=attachments['filename']
            attc="https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum+"&file="+dlattach
            print(attc)
            mailbox_vieww='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body+'\n\n'+'[Download]('+attc+') Attachments'
            filedl=wget.download(attc)
            await query.edit_message_text(mailbox_vieww,reply_markup=buttons)
            os.remove(dlattach)
    
 #MAINE CM
    elif query.data == "adl":
        await query.message.edit_text(
            text=ADL_TEXT,
            reply_markup=ADL_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
        
    elif query.data == "anl":
        await query.message.edit_text(
            text=ANL_TEXT,
            reply_markup=ANL_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif query.data == "grp":
        await query.message.edit_text(
            text=GRP_TEXT,
            reply_markup=GRP_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif query.data == "oth":
        await query.message.edit_text(
            text=OTH_TEXT,
            reply_markup=OTH_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
        
    elif query.data == "ext":
        await query.message.edit_text(
            text=EXT_TEXT,
            reply_markup=EXT_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "ext2":
        await query.message.edit_text(
            text=EXT2_TEXT,
            reply_markup=EXT2_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "ext3":
        await query.message.edit_text(
            text=EXT3_TEXT,
            reply_markup=EXT3_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
      
    elif query.data == "ext4":
        await query.message.edit_text(
            text=EXT4_TEXT,
            reply_markup=EXT4_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "mod":
        await query.message.edit_text(
            text=MOD_TEXT,
            reply_markup=MOD_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "adm":
        await query.message.edit_text(
            text=ADM_TEXT,
            reply_markup=ADM_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "ban":
        await query.message.edit_text(
            text=BAN_TEXT,
            reply_markup=BAN_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")
    elif query.data == "mas":
        await query.message.edit_text(
            text=MAS_TEXT,
            reply_markup=MAS_BUTTONS,
            disable_web_page_preview=True
        )
        await query.answer("👋Hey i am Gojo Satoru 𝕏 Bot")

    elif query.data == "close":
        await query.message.delete()
        await query.answer("Successfully Closed ❌")


#==========≠==


ADL_TEXT = """
__Use /reverse cmd to get reverse search via tracemoepy API
Note: This works best on uncropped anime pic,
when used on cropped media, you may get result but it might not be too reliable

Use /schedule cmd to get scheduled animes based on weekdays

Use /watch cmd to get watch order of searched anime

Use /fillers cmd to get a list of fillers for an anime

Use /quote cmd to get a random quote
Use /mquote cmd to gey more random quote

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
Use /askai or /mai Ask questions using ai for responding to user queries feom Gamini.
Use /aii Reply to image to containing text that you want transcripts, and  I'll process the image and provide you with the transcribed text.
Use /aicook Reply to image To get cooking instruction of the food in it.
Use /aiseller Reply to image and create you product desc.
Use /imagine Generate ai image from text
Use /gptai /gpt2 /iri /assis Ask anything to gpt ai.
Use /bard Ask anything to Bard ai.
Use /deep ask questions to Deep Ai.
Use /bing2 search any from Bing browser.
Use /info To get your information.
Use /ginfo, /cinfo To get Group informations.
Use /upscale Upscales your image quality.
Use /tagall or /mentionall to Mention all members in Group, or you can type /stop to mentioning to.
Use /tmail to generate your fakemail address.
Use /ping to ping me.__
"""
EXT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close"),
        InlineKeyboardButton("Next ➡️", callback_data="ext2")
        ]]
    ) 

EXT2_TEXT = """
**Extra module 2️⃣**
__Use /ranking /today to Check it out your Top ranking.
Use /nightmode To set your group night Mod.
Use /rmbg Reply to image to remove Background.
Use /sangmata_set [on/off] created simple detection to check user data include username, first_name, and last_name sangmata in groups.
Use /tmdb to get Move informations from The Movie Database [[TMDB](https://www.themoviedb.org)]
Use /unpic, /unrand to get images from [Unsplash](https://unsplash.com/)
Use /ocr [reply to photo] Extract Text From Image.
**Whisper:**
Use `@GojoSatoru_Xbot (Target Username or ID) (Your Message)` In inline to use this on group.
Use /imdb [Movename/Series Name]­ Get information about a Movie/Series­.
Use /googleimg It retrieves and displays images obtained through a Google image search.
Use /google_search To get Google search result with links.
Use /bingimg It retrieves and displays images obtained through a Bing image search.
Use /bingsearch To get Bing search result with links.
Use /news_search To search Latest news.
Use /wikisearch To Search Wikipedia quarys. 
"""
EXT2_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="ext"),
        InlineKeyboardButton("❌ Cancel", callback_data="close"),
        InlineKeyboardButton("Next ➡️", callback_data="ext3")
        ]]
    ) 

EXT3_TEXT = """
**Extra module 3️⃣**
__Use /meme cmd to get meme from meme api.
Use /mormeme cmd to get more memes.
Use /reddit cmd to get Random image from Reddit.
Use /morddit cmd to get more images from Reddit.
Use /unsplash cmd then your text to get images from unsplash.
Use /pexi cmd to get images from **Pexels**
Use /pexv cmd to get Videos from **Pexels**
Use /tor cmd to get Torrent movies links.
Use /repo the repository name to get GitHub repos.
Use /google cmd to get 10 quarys from Google.
Use /bingt cmd to get 10 quarys from Bing browser.
Use /yandex cmd to get 10 quarys from Yandex browser.
Use /ddg cmd to get 10 quarys from DuckDuckGo browser.
Use /ggimg cmd to get 10 Images from Google.
Use /bingimg cmd to get 10 Images from Bing.
Use /yandeximg cmd to get 10 Images from Yandex.
Use /ddgimg cmd to get 10 Images from DuckDuckGo.
Use /pimg cmd to get 6 images from Pinterest.
× [Auto welcome & Auto Left] Just add me to your group, and i will greetings | left, to New members with my advansed future.__
"""
EXT3_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="ext2"),
        InlineKeyboardButton("❌ Cancel", callback_data="close"),
        InlineKeyboardButton("Next ➡️", callback_data="ext4")
        ]]
    ) 


EXT4_TEXT = """
**Extra module 4️⃣**
Use /afk [Reason > Optional] - Tell others that you are AFK (Away From Keyboard).
/afk [reply to media] - AFK with media.
Adds MongoDB to database so that u can access­ Database 
Use /adddb [mongo uri]­ Get access to the MongoDB uri u added using /adddb & and type /showdb­.
Use /q [reply to a text message / give text as input] to Converts your text into a quote­
Use /wallpapers To Get random Wallpapers
Use /webgame To play web Games here.
Use /downl To save your photos and files to local server and /upload to get your saved files.
Use /paste [reply to message/text file]­ to Pastes the given text in spacebin­.

Use /txt_qr [text] To Convert Text to QR Code.
Use /qr_txt [Reply to qr photo] recognise qr code form given image.
Use /couples Get Todays Couples Of The Group In Interactive View
Use /figlet make finglet of the given text
Use /short | /unshort [link] ex: /short t.me/GojoSatoru_Xbot
Use /zip Reply to file to zip files.
Use /unzip Reply to Zipped files to separates files from zip.
"""
EXT4_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="ext3"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

MOD_TEXT = """
Click the below buttons to find out my Group Admin commands! [👮📝]
"""
MOD_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("👮Admin", callback_data="adm")
        ],[
        InlineKeyboardButton("🔰Ban", callback_data="ban")
        ],[
        InlineKeyboardButton("💥MassAction", callback_data="mas")
        ],[
        InlineKeyboardButton("⬅️ Back", callback_data="hlp"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

ADM_TEXT = """
**Group Admins only**:

/admins to know group admins.
/title (query) custom admin title.
/purge reply to message and bot delete your msg to reply message and also instead all msgs. 
/del delete a message.
/glink get group private link.
/cglink creat group new link.
/promote promote a member to admin.
/mpromote medium promote a member to admin.
/fpromote full promote a member to admin.
/demote demote a admin to member.
/setgphoto set group profile photo.
/setgtitle set group title.
/setgdesc set group description.
/pin reply to message and pin.
/unpin reply to pinned message to unpin.
/zombies send this to group to remove deleted accounts.
"""
ADM_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="mod"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

BAN_TEXT = """
**Group Admins only**:

Some people need to be publicly banned; spammers, annoyances, or just trolls.
This module allows you to do that easily, by exposing some common actions, so everyone will see!

!kick **kick the user.**
**Example:**
/kick id + reason
/kick reply to user + reason.

!ban **ban the user.**
**Example:**
/ban id + reason
/ban reply to user + reason.
/unban reply to user or give id to unban!.

!mute: **mute the user.**
**Example:**
/mute id + reason
/mute reply to user + reason.

!warn: **warn the user.**
Maximum Warns 3 if the user got 3 the we'll get banned  in your chat
to warn member in your group use:
/warn 123456789
/warn reply to user
you want to remove users warning use: /clearwarns
check user warn count use: /warns
"""
BAN_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="mod"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

MAS_TEXT = """
**Group Admins only**:

**Mass Action**
Only work for group owners!

/banall ban all members from group.
/kickall kick all members from group.
/unbanall unban all members from group.

to avoid service messages use instead "s"
for example: /skickall /sbanall.
"""
MAS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️ Back", callback_data="mod"),
        InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]]
    ) 

#==================•BROADCAST•==================
@anibot.on_message(filters.private & filters.command(["broadcast", "send"]))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
    else:
        await broadcast(m, db)

@anibot.on_message(filters.private & filters.command("stat"))
async def tsts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    sat = await m.reply_text(
        text=f"**Total Users in Database 📂:** `{await db.total_users_count()}`\n\n**Total Users with Notification Enabled 🔔 :** `{await db.total_notif_users_count()}`",
        quote=True
    )
    await m.delete()
    await asyncio.sleep(180)
    await sat.delete()

@anibot.on_message(filters.private & filters.command("ban_user"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

@anibot.on_message(filters.private & filters.command("unban_user"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )

@anibot.on_message(filters.private & filters.command("banned_users"))
async def banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"🆔**User_id** : `{user_id}`\n⏱️**Ban Duration** : `{ban_duration}`\n\n📆**Banned on** : `{banned_on}`\n\n💁**Reason**: `{ban_reason}`\n\n😌 @Musicx_dlbot"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)
