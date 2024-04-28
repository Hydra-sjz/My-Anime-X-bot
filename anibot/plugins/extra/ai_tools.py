import os, time
import openai
import random
from pyrogram import filters, Client
import requests
from anibot import anibot as app
from pyrogram.enums import ChatAction, ParseMode
from gtts import gTTS
import requests
import requests as r
from config import GPT_API, DEEP_API
from pyrogram.errors import MediaCaptionTooLong

from pyrogram.types import Message, InputMediaPhoto
# ----------------------------------------
# ----------------------------------------
openai.api_key = GPT_API

api_key = DEEP_API

API_URL = "https://sugoi-api.vercel.app/search"

# ----------------------------------------



#(;)-8-8
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

@app.on_message(filters.command(["gptai"]))
async def chatgptt(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide a query.**")

    query = " ".join(message.command[1:])    
    txt = await message.reply_text("**Wait patiently, requesting to API...**")
    await txt.edit("💭")
    api_response, error_message = fetch_data(api_url_gpt, query)
    await txt.edit(api_response or error_message)

#(:8:8

@app.on_message(filters.command(["bard", "gemini"]))
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
@app.on_message(filters.command(["gpt2"]))
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

@app.on_message(filters.command(["iri" , ]))
async def chat(app :app, message):
    
    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**Example:-**`/ask How to set girlfriend ?`")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            await message.reply_text(f"{x}")     
    except Exception as e:
        await message.reply_text(f"**Error**: {e} ")        


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.on_message(filters.command(["assis"]))
async def chat(app :app, message):
    
    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**Example:-**`.assis How to set girlfriend ?`")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            text = x    
            tts = gTTS(text, lang='en')
            tts.save('output.mp3')
            await app.send_voice(chat_id=message.chat.id, voice='output.mp3')
            os.remove('output.mp3')            
            
    except Exception as e:
        await message.reply_text(f"**Error**: {e} ") 
        
        
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.on_message(filters.command(["deep"]))
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
        await message.reply_text(f"**Error**: {e}")


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------

@app.on_message(filters.command(["bing2"]))
async def bing_search(app, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(
            message.command[1:]
        )  # Assuming the keyword is passed as arguments
        params = {"keyword": keyword}
        response = r.get(API_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("\x74\x69\x74\x6C\x65", "")
                    link = result.get("\x6C\x69\x6E\x6B", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
