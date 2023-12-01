from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument
from PIL import Image

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db

import os
import re
import time


def extract_episode_and_quality(filename):
    # Pattern 1: S1E01 or S01E01 with quality
    pattern_season_episode_quality = re.compile(r'S(\d+)E(\d+).*?(\d{3,4}p)')

    # Pattern 2: S02 E01 with quality
    pattern_season_episode_space_quality = re.compile(r'S(\d+) E(\d+).*?(\d{3,4}p)')

    # Pattern 3: Episode Number After "E" or "-" with quality
    pattern_episode_separator_quality = re.compile(r'[E|-](\d+).*?(\d{3,4}p)')

    # Pattern 4: Standalone Episode Number with quality
    pattern_standalone_episode_quality = re.compile(r'(\d+).*?(\d{3,4}p)')

    # Pattern 5: Extract Season, Episode Number, and Quality
    pattern_season_episode_quality_alt = re.compile(r'S(\d+)\s*[E|EP]\s*(\d+).*?(\w+)(?=\d{3,4}p)')

    # Try each pattern in order
    for pattern in [
        pattern_season_episode_quality,
        pattern_season_episode_space_quality,
        pattern_episode_separator_quality,
        pattern_standalone_episode_quality,
        pattern_season_episode_quality_alt
    ]:
        match = re.search(pattern, filename)
        if match:
            # Extracted season, episode numbers, and quality
            season_number = match.group(1) or match.group(3)
            episode_number = match.group(2) or match.group(4)
            quality = match.group(3) or match.group(4)  # Extracted quality
            return season_number, episode_number, quality

    # Return None if no pattern matches
    return None, None, None
    
@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")

# Inside the handler for file uploads
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)

    if not format_template:
        return await message.reply_text("Please set an auto rename format first using /autorename")

    # Extract information from the incoming file name
    if message.document:
        file_name = message.document.file_name
        media_type = "document"
    elif message.video:
        file_name = f"{message.video.file_name}.mp4"
        media_type = "video"
    elif message.audio:
        file_name = f"{message.audio.file_name}.mp3"
        media_type = "audio"
    else:
        return await message.reply_text("Unsupported file type")

    print(f"Original File Name: {file_name}")

    season_number, episode_number, quality = extract_episode_and_quality(file_name)

    # Check if any of the extracted values are missing
    if season_number is None or episode_number is None or quality is None:
        return await message.reply_text("Contact @Trippy_xt")

    print(f"Extracted Season Number: {season_number}")
    print(f"Extracted Episode Number: {episode_number}")
    print(f"Extracted Quality: {quality}")

    new_file_name = format_template.format(season=season_number, episode=episode_number, quality=quality)
    await message.reply_text(f"File renamed successfully to: {new_file_name}")
    
    _, file_extension = os.path.splitext(file_name)
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
