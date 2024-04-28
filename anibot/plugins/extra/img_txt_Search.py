import json
import random
import wikipedia 
import aiohttp
from urllib.parse import quote
from pyrogram import filters, Client 
from pyrogram.types import InputMediaPhoto, Message
from anibot import anibot as Mbot
from httpx import AsyncClient, Timeout
# <=======================================================================================================>

BINGSEARCH_URL = "https://sugoi-api.vercel.app/search"
NEWS_URL = "https://sugoi-api.vercel.app/news?keyword={}"

# HTTPx Async Client
state = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

# <================================================ FUNCTION =======================================================>
async def search_google(query: str, limit: int = 10):
    results = []
    query = quote(query)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://customsearch.googleapis.com/customsearch/v1?q={query}&key=AIzaSyABKLWB_mLrepcEUTTXo5_p-DDT76ccjdU&cx=5d7ff60ca55a45503"
        ) as response:
            try:
                resp = await response.json()
            except Exception:
                return None

    for i in resp["items"]:
        if len(results) >= limit:
            break

        result = {}
        try:
            result["title"] = i["title"]
            result["link"] = i["link"]
            result["description"] = i["snippet"]
            results.append(result)
        except Exception:
            pass

    return results


@Mbot.on_message(filters.command("google_search"))
async def google(bot, message):
    gs = await message.reply_text("__Your request is Processing...__")
    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        await gs.edit(
            "__give me some input to search Google 🔎\ne.g: /google_search [your_quary]__"
        )
        return
    results = await search_google(query)

    titles = []
    links = []
    descriptions = []
    for result in results:
        titles.append(result["title"])
        links.append(result["link"])
        descriptions.append(result["description"])

    msg = ""
    for tt, lik, des in zip(titles, links, descriptions):
        msg += f"[{tt}]({lik})\n`{des}`\n\n"
    await gs.edit("🔎 **Google Search**:\n`" + query + "`\n\n**Results:**\n" + msg, disable_web_page_preview=True)



@Mbot.on_message(filters.command("wikisearch"))
async def wikipediasearch(_, message: Message):
    query =  message.text.split(None, 1)[1] 
    if not query:
        await message.reply_text("__Give me some input to search Wikipedia...__\ne.g: `/wikisearch [your_query]`")
        return
    results = wikipedia.search(query)
    result = ""
    for s in results:
        try:
            page = wikipedia.page(s)
            url = page.url
            result += f"× [{s}]({url}) \n"
        except BaseException:
            pass
    await message.reply_text(
        "🔎 **WikiPedia Search:** {} \n\n**Result:** \n{}".format(query, result))

@Mbot.on_message(filters.command("newssearch"))
async def news(_, message: Message):
    keyword = (
        message.text.split(" ", 1)[1].strip() if len(message.text.split()) > 1 else ""
    )
    url = NEWS_URL.format(keyword)

    try:
        response = await state.get(url)  # Assuming state is an asynchronous function
        news_data = response.json()

        if "error" in news_data:
            error_message = news_data["error"]
            await message.reply_text(f"Error: {error_message}")
        else:
            if len(news_data) > 0:
                news_item = random.choice(news_data)

                title = news_item["title"]
                excerpt = news_item["excerpt"]
                source = news_item["source"]
                relative_time = news_item["relative_time"]
                news_url = news_item["url"]

                message_text = f"**Title**: {title}\n**Source**: {source}\n**Time**: {relative_time}\n**Excerpt**: {excerpt}\n**Link**: {news_url}"
                await message.reply_text(message_text)
            else:
                await message.reply_text("`No news found.`")

    except Exception as e:  # Replace with specific exception type if possible
        await message.reply_text(f"Error: {str(e)}")


@Mbot.on_message(filters.command("bingsearch"))
async def bing_search(client: Client, message: Message):
    try:
        if len(message.command) == 1:
            await message.reply_text("__Give me some input to search BingSearch.\ne.g: /bingsearch [your_query]...__")
            return

        keyword = " ".join(
            message.command[1:]
        )  # Assuming the keyword is passed as arguments
        params = {"keyword": keyword}

        response = await state.get(
            BINGSEARCH_URL, params=params
        )  # Use the state.get method

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("`No results found.`")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("`Sorry, something went wrong with the search.`")
    except Exception as e:
        await message.reply_text(f"`An error occurred: {str(e)}`")


# Command handler for the '/bingimg' command
@Mbot.on_message(filters.command("bingimg"))
async def bingimg_search(client: Client, message: Message):
    try:
        text = message.text.split(None, 1)[
            1
        ]  # Extract the query from command arguments
    except IndexError:
        return await message.reply_text(
            "__Give me some input to search Bing Images...\ne.g: /bingimg [your_query]...__"
        )  # Return error if no query is provided

    search_message = await message.reply_text("🔎")  # Display searching message

    # Send request to Bing image search API using state function
    bingimg_url = "https://sugoi-api.vercel.app/bingimg?keyword=" + text
    resp = await state.get(bingimg_url)
    images = json.loads(resp.text)  # Parse the response JSON into a list of image URLs

    media = []
    count = 0
    for img in images:
        if count == 7:
            break

        # Create InputMediaPhoto object for each image URL
        media.append(InputMediaPhoto(media=img))
        count += 1

    # Send the media group as a reply to the user
    await message.reply_media_group(media=media)

    # Delete the searching message and the original command message
    await search_message.delete()
    


# Command handler for the '/googleimg' command
@Mbot.on_message(filters.command("googleimg"))
async def googleimg_search(client: Client, message: Message):
    try:
        text = message.text.split(None, 1)[
            1
        ]  # Extract the query from command arguments
    except IndexError:
        return await message.reply_text(
            "__Give me some input to search Google image...\ne.g: /googleimg [your_query]...__"
        )  # Return error if no query is provided

    search_message = await message.reply_text("🔎")  # Display searching message

    # Send request to Google image search API using state function
    googleimg_url = "https://sugoi-api.vercel.app/googleimg?keyword=" + text
    resp = await state.get(googleimg_url)
    images = json.loads(resp.text)  # Parse the response JSON into a list of image URLs

    media = []
    count = 0
    for img in images:
        if count == 7:
            break

        # Create InputMediaPhoto object for each image URL
        media.append(InputMediaPhoto(media=img))
        count += 1

    # Send the media group as a reply to the user
    await message.reply_media_group(media=media)

    # Delete the searching message and the original command message
    await search_message.delete()
    
