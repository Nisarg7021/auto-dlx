from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument
from PIL import Image

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db

import os
import time
import re

# Modified Pattern 1: S1 E01 or S01 E01
pattern1 = re.compile(r'S(\d+) (?:E|EP)(\d+)')

# Modified Pattern 2: S02 E01
pattern2 = re.compile(r'S(\d+) (?:E|EP)(\d+)')

# Modified Pattern 3: Episode Number After "E" or "-"
pattern3 = re.compile(r'[E|-|EP](\d+)')

# Modified Pattern 4: Standalone Episode Number
pattern4 = re.compile(r'(\d+)')

# Quality Extraction Pattern
quality_pattern = re.compile(r'\b(?:1440p|2160p|144p|240p|360p|480p|720p|1080p|HdRip 2k|4k)\b', re.IGNORECASE)

def extract_episode_number(filename):
    # Try Quality Extraction Pattern
    quality_matches = quality_pattern.findall(filename)
    if quality_matches:
        print("Extracted Qualities:", quality_matches)

    # Try Pattern 1
    match = re.search(pattern1, filename)
    if match:
        return match.group(2)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(pattern2, filename)
    if match:
        return match.group(2)  # Extracted episode number

    # Try Pattern 3
    match = re.search(pattern3, filename)
    if match:
        return match.group(1)  # Extracted episode number

    # Try Pattern 4
    match = re.search(pattern4, filename)
    if match:
        return match.group(1)  # Extracted episode number
    
    # Return None if no pattern matches
    return None

# Example Usage:
filename = "One Piece S1-07 [720p][Dual] @Anime_Edge.mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

    
@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")

@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()

    # Save the preferred media type to the database
    await db.set_media_preference(user_id, media_type)

    await message.reply_text(f"Media preference set to: {media_type}")

# Inside the handler for file uploads
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)
    media_preference = await db.get_media_preference(user_id)

    if not format_template:
        return await message.reply_text("Please set an auto rename format first using /autorename")

    # Extract information from the incoming file name
    if message.document:
        file_name = message.document.file_name
        media_type = media_preference or "document"  # Use preferred media type or default to document
    elif message.video:
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"  # Use preferred media type or default to video
    elif message.audio:
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"  # Use preferred media type or default to audio
    else:
        return await message.reply_text("Unsupported file type")

    print(f"Original File Name: {file_name}")

    # Extract episode number and qualities
    episode_number = extract_episode_number(file_name)
    qualities = quality_pattern.findall(file_name)
    
    print(f"Extracted Episode Number: {episode_number}")
    print(f"Extracted Qualities: {qualities}")

    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

        # Add extracted qualities to the format template
        if qualities:
            placeholders = ["quality", "Quality", "QUALITY", "{quality}"]
            for placeholder in placeholders:
                format_template = format_template.replace(placeholder, str(qualities), 1)

        await message.reply_text(f"File renamed successfully to: {format_template}")

        _, file_extension = os.path.splitext(file_name)
        new_file_name = f"{format_template}{file_extension}"
        file_path = f"downloads/{new_file_name}"
        file = message

        ms = await message.reply("Trying to download...")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
        except Exception as e:
            return await ms.edit(e)     

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

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")

        await ms.edit("Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....")

        try:
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                await client.send_document(
                    message.chat.id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", ms, time.time())
                )
            elif type == "video":
                await client.send_video(
                    message.chat.id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", ms, time.time())
                )
            elif type == "audio":
                await client.send_audio(
                    message.chat.id,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", ms, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return await ms.edit(f"Error: {e}")

        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
