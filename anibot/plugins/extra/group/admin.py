from pyrogram import enums
from pyrogram import filters
from pyrogram.types import *
from pyrogram.errors import AdminRankInvalid
from datetime import datetime as time


from config import CMDS, DEVS, BOT_ID

from anibot import anibot as Nandha

from anibot.utils2.help.admin import *



@Nandha.on_message(filters.command(["rdacc","removezombies"], CMDS))
async def remove_delete_acc(_, message):
     user_id = message.from_user.id
     chat_id = message.chat.id
     if await is_admin(chat_id,user_id) == False: return await message.reply("`Admins Only!`")
     elif await can_ban_members(chat_id,user_id) == False: return await message.reply("`You Don't Have Ban Rights!`") 
     elif message.chat.type == enums.ChatType.PRIVATE: return await message.reply("`This Command Only work in Groups!`")
     else:
       try:
          done = 0
          msg = await message.reply("**Removing Deleted Accounts!**")
          async for m in Nandha.get_chat_members(chat_id):
              if m.user.is_deleted == True: 
                  await Nandha.ban_chat_member(chat_id,m.user.id)
                  done +=+1
          await msg.edit("**Successfully Removed Deleted Accounts**: `{}`".format(done))
       except Exception as e:
           print(e)



@Nandha.on_message(filters.command("title", CMDS))
async def set_admin_title(_, message):
     chat_id = message.chat.id
     user_id = message.from_user.id
     reply = message.reply_to_message
     if (await is_admin(chat_id,user_id)) == False:
        return await message.reply("`Admins Only`")
     elif (await is_admin(chat_id, BOT_ID)) == False:
        return await message.reply("`I Don't Have Rights!`")
     else:
        try:
           if len(message.text.split()) <2:
               return await message.reply("`Input New Admin Title!`")
           elif reply:
                  user_id = reply.from_user.id
                  title = message.text.split(None,1)[1]
           elif not reply:
                  user_id = int(message.text.split()[1])
                  title = message.text.split(None,2)[2]
           await Nandha.set_administrator_title(chat_id, user_id, title=title)
           await message.reply("**Successfully Admin**\n**Title Changed To: {}**".format(title))
        except Exception as e: return await message.reply(e)


@Nandha.on_message(filters.command(["glink","grouplink"], CMDS))
async def group_link(_, message):
     chat_id = message.chat.id
     user_id = message.from_user.id
     if (await is_admin(chat_id,user_id)) == False:
         return await message.reply("`Admins Only`")
     elif (await is_admin(chat_id, BOT_ID)) == False:
         return await message.reply("`I Don't Have Rights!`")
     else:
         try:
            link = (await Nandha.get_chat(chat_id)).invite_link
            await message.reply(link)
         except Exception as e: return await message.reply(e)

@Nandha.on_message(filters.command(["cglink","cgrouplink"], CMDS))
async def group_link(_, message):
     chat_id = message.chat.id
     user_id = message.from_user.id
     if (await is_admin(chat_id,user_id)) == False:
         return await message.reply("`Admins Only`")
     elif (await is_admin(chat_id, BOT_ID)) == False:
         return await message.reply("`I Don't Have Rights!`")
     else:
         try:
            link = await Nandha.export_chat_invite_link(chat_id)
            await message.reply(link)
         except Exception as e: return await message.reply(e)


@Nandha.on_message(filters.command(["setgdes","setgdesc"], CMDS))
async def chat_description(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    reply = message.reply_to_message
    if message.chat.type == enums.ChatType.PRIVATE:
          return await message.reply("`This Command work Only In Groups!`")
    elif (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
         return await message.reply_text("`Only Admins!`")
    elif (await can_change_info(chat_id,user_id)) == False or user_id not in DEVS:
         return await message.reply_text("`You Don't have Enough Rights to Do This!`")
    else:
         if not reply or reply and not reply.text:
               return await message.reply("reply to message text to set chat description!")
         desc = reply.text
         if len(desc) >250:
               return await message.reply("description is to much text please remove some wards and try again!")
         else:
             try:
                await Nandha.set_chat_description(chat_id, description=desc)
                await message.reply("Successfully Description Added!")
             except Exception as e:
                await message.reply(e)

@Nandha.on_message(filters.command("del", CMDS))
async def delete(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    reply = message.reply_to_message
    if message.chat.type == enums.ChatType.PRIVATE:
          if not reply:
              return await message.reply("`reply to message to delete!`", quote=True)
          await reply.delete()
          await message.delete()
    else:
        if (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
             return await message.reply("`Admins Only!`")
        elif (await can_delete_messages(chat_id,user_id)) == False and user_id not in DEVS:
             return await message.reply("`you don't have enough rights to do this!`")
        else:
            if (await is_admin(chat_id, BOT_ID)) == False:
                 return await message.reply("`Im not Admin!`")
            elif (await can_delete_messages(chat_id, BOT_ID)) == False:
               return await message.reply("`I don't have enough rights to do this!`")
            else:
               if not reply:
                     return await message.reply("`reply to message to delete!`")
               await reply.delete()
               await message.delete()
    

@Nandha.on_message(filters.command("purge", CMDS))
async def purge(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    reply = message.reply_to_message
    if message.chat.type == enums.ChatType.PRIVATE:
           start = time.now()
           message_ids = []
           for ids in range(reply.id, message.id +0):
              message_ids.append(ids)
           await Nandha.delete_messages(chat_id, message_ids, revoke=True)
           end = time.now()
           delete_time = (end - start).seconds / 10000
           return await message.reply_text(f"**Success Purged {delete_time}s!**")
    if (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`Admins Only!`")
    elif (await can_delete_messages(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`You Don't have Enough Rights to Do This!`")
    else:
          if (await is_admin(chat_id, BOT_ID)) == False:
               return await message.reply("`Make you Sure I'm Admin!`")
          elif (await can_delete_messages(chat_id,user_id)) == False:
               return await message.reply("`I Don't have Enough Rights to Do This!`")
          else:
                if reply:
                     message_reply_id = reply.id
                     message_id = message.id
                elif not reply:
                      return await message.reply("`Reply to Message for purge!`")
                start = time.now()
                message_ids = []
                for ids in range(message_reply_id, message_id +0):
                     message_ids.append(ids)
                await Nandha.delete_messages(chat_id, message_ids, revoke=True)
                end = time.now()
                y = (end - start).seconds / 10000
                await message.reply(f"**Success Purged {y}s!**")


@Nandha.on_message(filters.command(["admins","adminlist"], CMDS))
async def admins(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.chat.type == enums.ChatType.PRIVATE:
         return await message.reply("`This Command work Only In Groups!`")
    users = "👮 **Users**:\n"
    bots = "\n🤖 **Bots**:\n"
    async for admin in Nandha.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
           if admin.user.is_bot == False:
               users += f"• **{admin.user.first_name}** - (`{admin.user.id}`)\n"
           elif admin.user.is_bot == True:
               bots += f"• **{admin.user.first_name}** - (`{admin.user.id}`)\n"
    await message.reply(text=(users+bots))
              


@Nandha.on_message(filters.command("setgphoto", CMDS))
async def setchatphoto(_, message):
     chat_id = message.chat.id
     user_id = message.from_user.id
     reply = message.reply_to_message
     if message.chat.type == enums.ChatType.PRIVATE:
         return await message.reply("`This Command work Only In Groups!`")
     elif (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply_text("`Only Admins!`")
     elif (await can_change_info(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply_text("`You Don't have Enough Rights to Do This!`")
     else:
         if reply and not reply.media:
               return await message.reply("`please reply to a photo or document file to insert photo!`")   

         elif reply and reply.media:
              photo = await reply.download() 
         elif not reply and len(message.text.split()) >1:
                  photo = await Nandha.download_media(message.text.split(None, 1)[1])
         elif not reply and len(message.text.split()) <2:
              return await message.reply("`give me a photo id or reply to photo!`")
         if (await is_admin(chat_id, BOT_ID)) == False:
                     return await message.reply("`Make you sure I'm Admin!`")
         else:
             await Nandha.set_chat_photo(chat_id=chat_id,photo=photo)
             await message.reply("**Successfully New Photo Insert!**")



@Nandha.on_message(filters.command("setgtitle", CMDS))
async def setchattitle(_, message):
     chat_id = message.chat.id
     user_id = message.from_user.id
     reply = message.reply_to_message
     if message.chat.type == enums.ChatType.PRIVATE:
         return await message.reply("`This Command work Only In Groups!`")
     elif (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
         return await message.reply_text("`Only Admins!`")
     elif (await can_change_info(chat_id,user_id)) == False and user_id not in DEVS:
         return await message.reply_text("`You Don't have Enough Rights to Do This!`")
     else:
         if reply:
             title = reply.text         
         elif not reply and len(message.text.split()) <2:
                return await message.reply("`give a title or reply to a message to set title!`")
         elif not reply and len(message.text.split()) >1:  
                title = message.text.split(None,1)[1]
         if (await is_admin(chat_id, BOT_ID)) == False:
                return await message.reply("`Make you sure I'm Admin!`")
         else:
             await Nandha.set_chat_title(chat_id, title=title)
             await message.reply("`Successfully New title Inputed!`")
             




@Nandha.on_message(filters.command(["promote","fpromote","mpromote"], CMDS))
async def promoting(_, message):
       reply = message.reply_to_message
       chat_id = message.chat.id
       user_id = message.from_user.id
       if message.chat.type == enums.ChatType.PRIVATE:
         return await message.reply("`This Command work Only In Groups!`")
       elif (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`Admins Only!`")
       elif (await can_promote_members(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`You Don't Have Enough Rights!`")
       else:
                bot = await Nandha.get_chat_member(chat_id, BOT_ID)
                if reply and len(message.text.split()) >1:
                     user_id = reply.from_user.id
                     admin_title = message.text.split(None,1)[1]
                elif reply and len(message.text.split()) <2:
                      user_id = reply.from_user.id
                      admin_title = "Admin"
                elif not reply and len(message.text.split()) >1:
                      user_id = message.text.split()[1]
                      admin_title = message.text.split(None,2)[2]
                elif not reply and len(message.text.split()) <3:
                     user_id = message.text.split()[1]
                     admin_title = "Admin"                
                if (await is_admin(chat_id, BOT_ID)) == False:
                      await message.reply("`Make you sure I'm Admin!`")
                elif (await can_promote_members(chat_id, BOT_ID)) == False:
                      await message.reply("`I don't have enough rights to promote!`")
                elif (await is_admin(chat_id,user_id)) == True:
                      await message.reply("`User Already A Admin!`")
                else:
                   try:
                       if message.text[1] == "f":
                           await message.chat.promote_member(user_id=user_id,privileges=bot.privileges)
                           await Nandha.set_administrator_title(chat_id, user_id, title=admin_title)
                           await message.reply(f"**Successfully Full Promoted**!\n**Following Admin Title**:\n`{admin_title}`")
                       elif message.text[1] == "m":
                           await message.chat.promote_member(user_id=user_id,privileges=ChatPrivileges(
               can_invite_users=True,
               can_pin_messages=True,
               can_manage_video_chats=True))
                           await Nandha.set_administrator_title(chat_id, user_id, title=admin_title)
                           await message.reply(f"**Successfully Medium Promoted**!\n**Following Admin Title**:\n`{admin_title}`")
                       else:  
                           await message.chat.promote_member(user_id=user_id,privileges=ChatPrivileges(
               can_invite_users=True,
               can_delete_messages=True,
               can_restrict_members=True,
               can_pin_messages=True,
               can_manage_video_chats=True))
                           await Nandha.set_administrator_title(chat_id, user_id, title=admin_title)
                           await message.reply(f"**Successfully Full Promoted**!\n**Following Admin Title**:\n`{admin_title}`")
                   except AdminRankInvalid:
                      return await message.reply("`Input maximum 8 characters!`")



@Nandha.on_message(filters.command("demote", CMDS))
async def demoting(_, message):
       reply = message.reply_to_message
       chat_id = message.chat.id
       user_id = message.from_user.id
       if message.chat.type == enums.ChatType.PRIVATE:
         return await message.reply("`This Command work Only In Groups!`")
       elif (await is_admin(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`Admins Only!`")
       elif (await can_promote_members(chat_id,user_id)) == False and user_id not in DEVS:
            return await message.reply("`You Don't Have Enough Rights!`")
       else:
                bot = await Nandha.get_chat_member(chat_id, BOT_ID)
                if reply:
                     user_id = reply.from_user.id
                elif not reply and len(message.text.split()) <3:
                      user_id = message.text.split()[1]
                else:
                    return await message.reply("`reply to admin or give a userid to demote!`")
                              
                if (await is_admin(chat_id, BOT_ID)) == False:
                      await message.reply("`Make you sure I'm Admin!`")
                elif (await can_promote_members(chat_id, BOT_ID)) == False:
                      await message.reply("`I don't have enough rights to demote!`")
                else:
                   try:
                       await message.chat.promote_member(user_id=user_id,
                       privileges=ChatPrivileges(
               can_change_info=False,
               can_invite_users=False,
               can_delete_messages=False,
               can_restrict_members=False,
               can_pin_messages=False,
               can_promote_members=False,
               can_manage_chat=False,
               can_manage_video_chats=False))
                       await message.reply(f"**Successfully Demoted!**!") 
                   except Exception as e:
                      return await message.reply(e)


@Nandha.on_message(filters.command(["pin","unpin"], CMDS))
async def pin_unpin_chat_message(_, message):
       user = message.from_user
       chat = message.chat
       reply = message.reply_to_message
       if await is_admin(chat.id, user.id) == False:
            return await message.reply("Admins Only")
       elif await can_pin_messages(chat.id, user.id) == False:
            return await message.reply("You Need Can Pin Rights!")
       else:
           if await is_admin(chat.id, BOT_ID) == False:
               return await message.reply("Make Me Admin")
           elif await can_pin_messages(chat.id, BOT_ID) == False:
               return await message.reply("I Need Can Pin Rights!")
           else: 
              if not reply: return await message.reply("Reply to message!")
              if message.text[1:4] == "pin":
                   await reply.pin()  
                   return await message.reply("I Have Pinned This [Message]({})!".format(reply.link), disable_web_page_preview=True)
              elif message.text[1:6] == "unpin":
                    await reply.unpin()           
                    return await message.reply("I Have UnPinned This [Message]({})!".format(reply.link), disable_web_page_preview=True)
              else: return await message.reply("`Check Formatting And Do Correctly!`")
       

