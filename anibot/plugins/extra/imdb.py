from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ia = IMDb()


@Client.on_message(filters.command(["imdb"]))
async def search_movie(client, message):
    if len(message.command) < 2:
        await client.send_message(
            chat_id=message.chat.id,
            text="__Please provide a movie or TV series name after the /imdb command.__"
        )
        return
    # Get the movie name from the user's message 
    movie_name = message.text.split(" ", 1)[1]
    if len(movie_name) < 1:
        await client.send_message(
            chat_id=message.chat.id,
            text="__Please provide a movie or TV series name after the /imdb command.__"
        )
        return
    if len(str(movie_name)) > 40:
        await client.send_message(
            chat_id=message.chat.id,
            text="__Please provide a movie or TV series name. Not a paragraph! :)__"
        )
        return
    mv = await message.reply_photo("https://telegra.ph/file/45c3722c81365bb3d9a48.jpg", caption=f"`Searching for {movie_name}`\n\n**Powered by**: @XBOTS_X | ©️ @GojoSatoru_Xbot")
    movies = ia.search_movie(movie_name, results=10)
    if len(movies) == 0:
        await mv.edit("**__No movies found with that name!__**")
        return
    button_list = []
    for i, movie in enumerate(movies[:10]):
        button_list.append([InlineKeyboardButton(text=movie['title'], callback_data=f"{message.from_user.id}.more_details {movie.movieID} :{movie_name}:")])
    # button_list.append([InlineKeyboardButton(text="", callback_data=f"more_details {movie.movieID}")])
    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup(button_list)

    # Send a message to the user with the search results and buttons
    message_text = f"Found {len(movies)} results. Please select a movie:"
    await mv.edit(
        text=message_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
