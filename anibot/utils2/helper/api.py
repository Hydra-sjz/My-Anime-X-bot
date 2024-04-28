# Copyright 2023 Qewertyy, MIT Licence
from lexica import AsyncClient


async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    try:
        client = AsyncClient()
        content = await client.upscale(image)
        await client.close()
        upscaled_file_path = "upscaled.png"
        with open(upscaled_file_path, "wb") as output_file:
            output_file.write(content)
        return upscaled_file_path
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")

async def getFile(message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        image = await message.reply_to_message.download()
        return image
    else:
        return None
