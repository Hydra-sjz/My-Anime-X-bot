import os 
import time
import shutil
import asyncio
import zipfile
from pyrogram import Client, filters, errors

from anibot.utils2.helper.basic_helpers import progress

@Client.on_message(filters.command(["downl"]))
async def download_f(bot, message):
    dl = await message.reply_text("Downloading to Server..")
    if not message.reply_to_message:
        await dl.edit("`Reply to a message to download!")
        return
    if not message.reply_to_message.media:
        await dl.edit("`Reply to a message to download!`")
        return
    if message.reply_to_message.media or message.reply_to_message.document or message.reply_to_message.photo:
        c_time=time.time()
        file = await message.reply_to_message.download(progress=progress, progress_args=(dl, c_time, f"`Downloading This File!`")
    )
    file_txt = "__Downloaded This File To__ `{}`."
    filename = os.path.basename(file)
    f_name = os.path.join("downloads", filename)
    await dl.edit(file_txt.format(f_name))

@Client.on_message(filters.command(["upload"]))
async def upload_file(c, m):
    try:
        file = m.text.split(None, 1)[1]
    except IndexError:
        await m.reply_text("What should I upload??")
        return
    
    authorized_users = [1246467977, 1089528685]
    authorized_paths = ['downloads/', '/app/Mr.Stark/downloads/']
    
    if m.from_user.id not in authorized_users:
        if not any(file.startswith(path) for path in authorized_paths):
            await m.reply_text("You are unauthorized.")
            return

    msg = await m.reply_text("Uploading file, please wait...")
    try:
        c_time = time.time()
        await m.reply_document(file, progress=progress, progress_args=(msg, c_time, "Uploading This File!"))
    except FileNotFoundError:
        await msg.edit("No such file found.")
    finally:
        await msg.delete()

def unzip_file(zip_path, extract_dir):
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        for file_info in zip_ref.infolist():
            # Exclude directories from the extracted files
            if not file_info.is_dir():
                extracted_files.append(os.path.join(extract_dir, file_info.filename))
    return extracted_files


@Client.on_message(filters.command(["unzip"]))
async def unzip_files(c, m):
    reply = m.reply_to_message if m.reply_to_message else None
    try:
      zip_file = m.text.split(None, 1)[1]
    except IndexError:
      zip_file = None
    if not zipfile and reply:
      await m.reply_text("`What should I Unzip?`")
      return
    if reply and reply.document:
        document = reply.document
        if document.mime_type == 'application/zip':
            c_time=time.time()
            target_dir = f"downloads/unzip/{m.from_user.id}"
            try:
               await c.send_message(m.from_user.id, "**Files will be sent here**")
            except errors.PeerIdInvalid:
                 await m.reply_text("**Start Me in Pm First**")
                 return
            except errors.UserIsBlocked:
                 await m.reply_text("**Start Me in Pm First**")
                 return
            dl = await m.reply_text("`Downloading file...`")
            zip_file = await reply.download(progress=progress, progress_args=(dl, c_time, "`Downloading File!`"))
            await dl.edit("`Downloading Done!!\nNow Unzipping it...`")
            extracted_file_paths = unzip_file(zip_file, target_dir)
            await dl.edit(f"**Found {len(extracted_file_paths)} files**\n`Now Uploading...")
            for index, file in enumerate(extracted_file_paths, 1):
                 try:
                   await c.send_document(m.from_user.id, file)
                   await dl.edit(f"**Uploaded** `{index}/{len(extracted_file_paths)}`")
                # except errors.PeerIdInvalid:
                #     await dl.edit("**Start Me in Pm First**")
                # except errors.UserIsBlocked:
                #     await dl.edit("**Start Me in Pm First**")
                 except errors.FloodWait as e:
                     await asyncio.sleep(e.value)
                     await m.reply_document(file)
                 except:
                     continue
            await dl.edit("**All files have been sent to ur PM**")
            shutil.rmtree(target_dir)
            os.remove(zip_file)
        else:
            await m.reply_text("`The replied file is not a zip.`")
    else:
      await m.reply_text("`Reply to a Zip File to UnZip`")
