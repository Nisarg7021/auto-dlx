from pyrogram import Client, filters
from pyrogram.types import InputMediaDocument
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
import os
import re
import time
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db

def extract_episode_number(filename):
    # Patterns for extracting episode numbers
    patterns = [
        re.compile(r'S(\d+)E(\d+)'),
        re.compile(r'S(\d+) E(\d+)'),
        re.compile(r'[E|-](\d+)'),
        re.compile(r'(\d+)')
    ]

    # Try each pattern in order
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)  # Extracted episode number
    
    # Return None if no pattern matches
    return None

@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)

    if not format_template:
        return await message.reply_text("Please set an auto rename format first using /autorename")

    # Extract information from the incoming file name
    file_name = message.document.file_name if message.document else None
    if not file_name:
        return await message.reply_text("Unsupported file type")

    print(f"Original File Name: {file_name}")

    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")

    if episode_number:
        # Use the episode_number and format_template string to generate the new file name
        new_file_name = format_template.format(episode=episode_number)
        await message.reply_text(f"File renamed successfully to: {new_file_name}")

        # Assuming you have access to the required variables (format_template, episode_number, file_name)
        _, file_extension = os.path.splitext(file_name)
        file_path = f"downloads/{new_file_name}"

        ms = await message.reply("Trying to download...")
        try:
            path = await client.download_media(message=message, file_name=file_path, progress=progress_for_pyrogram)
        except Exception as e:
            return await ms.edit(str(e))

        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        ph_path = None
        c_caption = await db.get_caption(message.chat.id)
        c_thumb = await db.get_thumbnail(message.chat.id)

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
        elif message.document.thumbs:
            ph_path = await client.download_media(message.document.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")

        await ms.edit("Trying to upload...")
        type = message.document.mime_type.split("/")[0].lower()
        try:
            if type == "document":
                await client.send_document(
                    chat_id=message.chat.id,
                    document=file_path,
                    thumb=ph_path, 
                    caption=caption, 
                    progress=progress_for_pyrogram(ud_type, message, start))
            elif type in ["video", "audio"]:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram(ud_type, message, start))
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return await ms.edit(f"Error {e}")

        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
    else:
        await message.reply_text("Failed to extract the episode number from the file name. Please check the format.")
    
