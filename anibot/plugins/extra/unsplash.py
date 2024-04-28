from pyrogram import Client, filters
import requests
from pyrogram.types import Message
from io import BytesIO
from anibot import anibot as app


def get_random_picture():
    response = requests.get('https://source.unsplash.com/random')
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None  

@app.on_message(filters.command("unrand"))
def pic(client, message):
    random_pic = get_random_picture()
    if random_pic:
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
        message.reply_photo(random_pic)
    else:
        message.reply("Sorry, I couldn't get a random picture at the moment. 😔")



@app.on_message(filters.command("unpic"))
def pic_command(client, message: Message):
    # Extract the name from the command
    try:
        name = message.command[1]
    except IndexError:
        client.send_message(message.chat.id, "Please provide a name after the /unpic command.")
        return

   
    unsplash_url = f"https://source.unsplash.com/500x500/?{name}"

    try:
        response = requests.get(unsplash_url)
        if response.status_code == 200:
            client.send_photo(message.chat.id, photo=unsplash_url, caption=f"Here is the picture related to {name}.\n\n©️ @GojoSatoru_Xbot | @XBOTS_X" )
        else:
            client.send_message(message.chat.id, "❌Failed to fetch image.")
    except requests.RequestException as e:
        client.send_message(message.chat.id, f"😐An error occurred ➥ {str(e)}")        
