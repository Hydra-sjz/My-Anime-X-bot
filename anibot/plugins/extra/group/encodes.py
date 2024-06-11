
import re
from anibot import anibot as Nandha
from Nandha.help.encodes import *
from pyrogram import filters



@Nandha.on_message(filters.command(["decode","encode"]))
async def encodes(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id

      if reply and not reply.text:
          return await message.reply("`reply to message text!`")
      elif reply and reply.text:
           data = reply.text
      elif not reply and len(message.text.split()) <2:
             return await message.reply("`reply to text or give me some text to (en/de) code!`")
      elif not reply and len(message.text.split()) >1:
            data = message.text.split(None,1)[1]
      if re.search("en", message.text.split()[0]):
           await Nandha.send_message(chat_id, text=encode(data), reply_to_message_id=message.id)
      elif re.search("de", message.text.split()[0]):
           await Nandha.send_message(chat_id, text=decode(data), reply_to_message_id=message.id)


