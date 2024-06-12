from config import CMDS
from anibot import anibot as Nandha
from anibot.utils2.help import mongodb

from pyrogram import filters, enums
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied, UsernameInvalid
from pyrogram.types import *


from anibot.utils2.help.admin import is_admin, can_ban_members, can_change_info

db = mongodb.FSUB #db



def fsub_chats():
   chats = []
   for x in db.find():
      chats.append(x["chat_id"])
   return chats

@Nandha.on_message(filters.incoming, group=100)
async def ForceSub(_, message):
     chat_id = message.chat.id
     bot_id = Nandha.me.id
     if chat_id in fsub_chats():
          x = db.find_one({"chat_id": chat_id})
          fsub_channel = x["channel"]
          user_id = message.from_user.id
          if await is_admin(chat_id, bot_id) == False:
               return await message.reply_text("Make Me Admin Baka!")
          elif await can_ban_members(chat_id, bot_id) == False:
               return await message.reply_text("Give Me Restrict right to mute who don't sub a channel!")
          else:
     
              try:
                  xx = await Nandha.get_chat_member(fsub_channel, user_id)
              except UserNotParticipant:
                    link = (await Nandha.get_chat(fsub_channel)).invite_link
                    await Nandha.restrict_chat_member(chat_id, user_id, ChatPermissions())
                    await message.reply_text("I have mute you join my force sub channel and click the below button !",
                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("join Channel ✅", url=link),
                       InlineKeyboardButton("Unmute Me", callback_data=f"fsub_user:{user_id}"),]]))

                
@Nandha.on_callback_query(filters.regex("fsub_user"))
async def unmute_fsubbed(_, query):
       chat_id = query.message.chat.id
       user_id = int(query.data.split(":")[1])
       if not user_id == query.from_user.id:
           return await query.answer("This Button not for you Nimba!", show_alert=True)
       else:
           xx = db.find_one({"chat_id": chat_id})
           channel = xx["channel"]
           try:
              hmm = await Nandha.get_chat_member(chat_id=channel, user_id=user_id)
           except UserNotParticipant:
                 return await query.answer("you most join the force channel after click this button to unmute you!", show_alert=True)
           await Nandha.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
           return await query.message.edit("Thanks For Joining My Channel Now you can speak to members!")



@Nandha.on_message(filters.command("fsub", CMDS))
async def ForceSubscribe(_, message):
      chat_id = message.chat.id
      bot_id = Nandha.me.id
      user_id = message.from_user.id
      if message.chat.type == enums.ChatType.PRIVATE:
           return await message.reply_text("This Command Only work in Groups!") 
      if await is_admin(chat_id, user_id) == False:
            return await message.reply_text("Only group admins can Force sub a channel!")
      elif await can_change_info(chat_id, user_id) == False: 
            return await message.reply_text("You don't have can change group info rights!")
      try:
          message.text.split()[1]
      except: return await message.reply_text("Format: /fsub on/off")
      if message.text.split()[1] == "on":
           ASK = "okay send me Force Subscribe channel username." #chat.ask
           await message.reply_text( 
               text=ASK, 
               reply_to_message_id=message.id, reply_markup=ForceReply(selective=True))
           try:
               Fsub_channel = ASK.text
               hmm = await Nandha.get_chat_member(chat_id=Fsub_channel, user_id=bot_id)
           except UserNotParticipant:
                 return await message.reply_text("Add Me there and make me sure Am Admin!")
           except ChatAdminRequired:
                  return await message.reply_text(f"I don't have rights to check the user is a member in a channel please make me sure am admin in {Fsub_channel}")
           except UsernameNotOccupied:
                  return await message.reply_text(f"Double check channel username!")
           except UsernameInvalid:
                  return await message.reply_text(f"Invalid username is {Fsub_channel}")
           fsub_chat = await Nandha.get_chat(Fsub_channel)
           x = db.find_one({"chat_id": chat_id})
           if x:
              db.update_one({"chat_id": chat_id}, {"$set": {"channel": Fsub_channel}})
           else:
              db.insert_one({"chat_id": chat_id, "fsub": True, "channel": Fsub_channel})          
           return await message.reply_text(f"okay thanks for using and I have now Force Subscribed this group to {fsub_chat.title}")
      elif message.text.split()[1] == "off":
           x = db.find_one({"chat_id": chat_id})
           if x:
               db.delete_one(x)
               return await message.reply_text("okay removed {} channel Force Subscribe!".format(x["channel"]))
           else:
               return await message.reply_text("Semms like this chat don't have set any Force subs!")
      else:
           return await message.reply_text("Format: /fsub on/off")
             
