from config import CMDS, BOT_ID

from anibot import anibot as Nandha

from pyrogram.types import *
from pyrogram.errors import UserNotParticipant
from pyrogram import filters 
from anibot.utils2.help.admin import *
from anibot.utils2.help import mongodb
db = mongodb["WARNING"]


WARN_TEXT = """
WARNING!
**Name**: {name}
**UID**: [`{user_id}`]
**Reason**: `{reason}`
**Total warns**: [`{warns}`]
"""
WARN_B_TEXT = """
BANNED!
**Name**: {name}
**UID**: [`{user_id}`]
**Reached Maximum Warns**: [`{warns}`]
**Reason 1**: `{reason1}`
**Reason 2**: `{reason2}`
**Reason 3**: `{reason3}`
"""


async def is_warn_user(chat_id: int, user_id: int):
      x = db.find_one({"chat_id": chat_id, "user_id": user_id})
      if bool(x):
         return True
      else: return False

async def get_warn_count(chat_id: int, user_id: int):
    x = db.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = x["warn"]
    return warns

@Nandha.on_message(filters.command("warns", CMDS))
async def warns_check(_, message):
     chat = message.chat
     user = message.from_user
     if message.chat.type == enums.ChatType.PRIVATE: return await message.reply("Command Works Only On Groups!")
     elif await is_admin(chat_id=chat.id, user_id=user.id) == False:
           return await message.reply_text("Admins Only Can Warn Members!")
     else:
       reply = message.reply_to_message
       if reply: user_id = reply.from_user.id
       elif not reply and len(message.text.split()) >1: user_id = message.text.split()[1]
       else: return await message.reply_text("Invalid Method!")
       try:
          user = await Nandha.get_users(user_id)
       except Exception as e: return await message.reply(e)
       if await is_warn_user(chat_id=chat.id, user_id=user_id):
           warns = await get_warn_count(chat_id=chat.id, user_id=user_id)
           await message.reply_text(
                f"**{user.mention}'s warn** [`{warns}`]")
       else: return await message.reply_text("That User Don't Had Any Warns here!")


@Nandha.on_message(filters.command("clearwarns", CMDS))
async def clear_warns(_, message):
     user = message.from_user
     chat = message.chat
 
     if await is_admin(chat_id=chat.id, user_id=user.id) == False:
           return await message.reply_text("Admins Only Can Warn Members!")
     elif await can_ban_members(chat_id=chat.id, user_id=user.id) == False:  
           return await message.reply_text("You Needs a can_restrict_members Rights!")
     else:
       reply = message.reply_to_message
       if reply: user_id = reply.from_user.id
       elif not reply and len(message.text.split()) >1: user_id = message.text.split()[1]
       else: return await message.reply_text("Invalid Method!")
       x = db.find_one({"chat_id": chat.id, "user_id": user_id})
       user = await Nandha.get_users(user_id)
       if bool(x):
            db.delete_one(x)
            await message.reply_text("{} Successfully Warns Cleared!".format(user.mention))
            return
       else: return await message.reply_text("No Warns Restored in that ID!")

@Nandha.on_message(filters.command("warn", CMDS))
async def warn(_, message):
     user = message.from_user
     chat = message.chat
     if message.chat.type == enums.ChatType.PRIVATE:
           return await message.reply_text("This Command Only Work On Groups!")
     elif await is_admin(chat_id=chat.id, user_id=user.id) == False:
           return await message.reply_text("Admins Only Can Warn Members!")
     elif await can_ban_members(chat_id=chat.id, user_id=user.id) == False:  
           return await message.reply_text("You Needs a can_restrict_members Rights!")
     else:
         if await is_admin(chat_id=chat.id, user_id=BOT_ID) == False:
              return await message.reply_text("Make Me Admin First Baka!")
         elif await can_ban_members(chat_id=chat.id, user_id=BOT_ID) == False:  
              return await message.reply_text("I Needs a can_restrict_members Rights!")
         reply = message.reply_to_message
         if reply: 
               user_id = reply.from_user.id
               if len(message.text.split()) >1: reason = message.text.split(None,1)[1]
               else: reason = "No Reason Provide!"
         elif not reply and len(message.text.split()) == 2: 
               user_id = message.text.split()[1]
               if len(message.text.split()) >2:
                     reason = message.text.split(None,2)[2]
               else: reason = "No Reason Provide!"
         else: return await message.reply_text("Invalid Method!")
         try: 
            x = await message.chat.get_member(user_id)
            if x.is_member == False:
                 return await message.reply("that user not a Member here!")
         except UserNotParticipant: return await message.reply("that user not a Member here!")
         if await is_admin(chat_id=chat.id, user_id=user_id):
              return await message.reply_text("Your Trying to Warn A Admin I couldn't do that!")
         x = db.find_one({"chat_id": chat.id, "user_id": user_id})
         user = await Nandha.get_users(user_id)
         if bool(x):
             n_warn = int(x["warn"])+1
             db.update_one({"chat_id": chat.id, "user_id": user_id}, {"$set": {"warn": n_warn, f"reason {n_warn}": reason}})
             if n_warn > 2:
                  reason1 = x["reason 1"]
                  reason2 = x["reason 2"]
                  reason3 = reason
                  await Nandha.ban_chat_member(chat_id=chat.id, user_id=user.id)
                  await message.reply_text(WARN_B_TEXT.format(name=user.mention, user_id=user.id, warns=n_warn, reason1=reason1, reason2=reason2, reason3=reason3))
                  db.delete_one(x)
                  return
         else:
             ll = {"chat_id": chat.id, "user_id": user_id, "warn": 1, "reason 1":reason}
             db.insert_one(ll)
         x = db.find_one({"chat_id": chat.id, "user_id": user_id,})
         warns = int(x["warn"])
         return await message.reply_text(WARN_TEXT.format(name=user.mention, user_id=user.id, reason=reason, warns=warns))

