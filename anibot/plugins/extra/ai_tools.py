import os, time
import openai
import random
from pyrogram import filters, Client
import requests
from anibot import anibot as app
from pyrogram.enums import ChatAction, ParseMode
#from gtts import gTTS
import requests
import requests as r
from config import GPT_API, DEEP_API
from pyrogram.errors import MediaCaptionTooLong

from pyrogram.types import Message, InputMediaPhoto
# ----------------------------------------
# ----------------------------------------
openai.api_key = GPT_API

api_key = DEEP_API


# ----------------------------------------



@app.on_message(filters.command(["ai"],  prefixes=["/"]))
async def chat_gpt(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "Example:\n\n/chatgpt Where is TajMahal?"
            )
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://chatgpt.apinepdev.workers.dev/?question={a}')

            try:
                # Check if "results" key is present in the JSON response
                if "answer" in response.json():
                    x = response.json()["answer"]
                    end_time = time.time()
                    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
                    await message.reply_text(
                        f" {x}      ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛  @GojoSatoru_Xbot",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                # Handle any other KeyError that might occur
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"**á´‡Ê€Ê€á´Ê€: {e} ")

#=======
api_url_gpt = "https://nandha-api.onrender.com/ai/gpt"
api_url_bard = "https://nandha-api.onrender.com/ai/bard"

def fetch_data(api_url: str, query: str) -> tuple:
    try:
        response = requests.get(f"{api_url}/{query}")
        response.raise_for_status()
        data = response.json()
        return data.get("content", "No response from the API."), data.get("images", False)
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {e}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

@app.on_message(filters.command(["chatg1", "task", "gput"]))
async def chatgptt(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide a query.**")

    query = " ".join(message.command[1:])    
    txt = await message.reply_text("**Wait patiently, requesting to API...**")
    await txt.edit("💭")
    api_response, error_message = fetch_data(api_url_gpt, query)
    await txt.edit(api_response or error_message)

#==========

@app.on_message(filters.command(["tbard", "gemini"]))
async def bardb(_, message):
    chat_id = message.chat.id
    message_id = message.id
    
    if len(message.command) < 2:
        return await message.reply_text("Please provide a query.")

    query = " ".join(message.command[1:])
    txt = await message.reply_text("Wait patiently, requesting to API...")
    await txt.edit("💭")
    
    api_response, images = fetch_data(api_url_bard, query)

    medias = []
    bard = str(api_response)
    try:
       photo_url = images[-1]
    except:
        pass
    
    
    if images:
        if len(images) > 1:
            for url in images:
                medias.append(InputMediaPhoto(media=url, caption=None))
                        
            medias[-1] = InputMediaPhoto(media=photo_url, caption=bard)
            
            try:
                await app.send_media_group(chat_id=chat_id, media=medias, reply_to_message_id=message_id)
                return await txt.delete()
            except Exception as e:
                return await txt.edit(str(e))
        elif len(images) < 2:
            image_url = images[0]
            try:
                await message.reply_photo(photo=image_url, caption=bard)
                return await txt.delete()
            except MediaCaptionTooLong:
                return await txt.edit(bard)
            except Exception as e:
                return await txt.edit(str(e))
        else:
            return await txt.edit('Somthing went wrong')
    else:
        try:
            return await txt.edit(bard)
        except Exception as e:
            return await txt.edit(str(e))


# ----------------------------------------
@app.on_message(filters.command(["chatgpt2","ai","ask"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def chat(app :app, message):
    
    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-**`.ask How to set girlfriend ?`")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            await message.reply_text(f"{x}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.on_message(filters.command(["deep"],  prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def deepchat(app: app, message):
    name = message.from_user.first_name
    try:
        #await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}\nHow can I assist you today?.")
        else:
            a = message.text.split(' ', 1)[1]

            data = {
                'text': a,  
            }

            headers = {
                'api-key': api_key,
            }

            r = requests.post("https://api.deepai.org/api/text-generator", data=data, headers=headers)
            response = r.json()
            answer_text = response['output']
            await message.reply_text(f"{answer_text}")
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e}")


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

@app.on_message(filters.command(["qu" , ],  prefixes=["e","E"]))
async def deepchat(app: app, message):
    name = message.from_user.first_name
    try:
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(f"Hello {name}\n How can I assist you today?.")
        else:
            a = message.text.split(' ', 1)[1]

            data = {
                'text': a,  
            }

            headers = {
                'api-key': api_key,
            }

            r = requests.post("https://api.deepai.org/api/text-generator", data=data, headers=headers)
            response = r.json()
            answer_text = response['output']
            await message.reply_text(f"{answer_text}")
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

# -----------------------------------------------------------------------------------
