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
import re

def extract_episode_number(filename):
    # Improved Pattern for Episode Number Extraction
    pattern_additional = re.compile(r'S(\d{1,2})[^\d]|(\d{1,2})(?![\d\s]*[E|EP]|-[^\d]|[^E|EP|-])', re.IGNORECASE)

    # Additional Pattern for "High_School_DxD_S2_01_1080pDual_@Anime_Crimson@Anime_Sensei_Network.mkv"
    pattern = re.compile(r'_(\d{1,2})_', re.IGNORECASE)

    match = re.search(pattern, filename)
    if match:
        episode_number = match.group(1) or match.group(2)  # Extracted episode number
        print(f"Pattern {pattern.pattern} matched. Extracted episode number: {episode_number}")
        return episode_number

    # Check the additional pattern
    match_additional = re.search(pattern_additional, filename)
    if match_additional:
        episode_number_additional = match_additional.group(1)
        print(f"Pattern {pattern_additional.pattern} matched. Extracted episode number: {episode_number_additional}")
        return episode_number_additional

    # Return None if no pattern matches
    return None

# Test the function with examples
filenames = [
    "S1E1",
    "S01E1",
    "S02 E1",
    "S02 E01",
    "One Piece S1-7",
    "One Piece S1-07",
    "One Piece 2000",
    "E07 Example Anime",
    "Anime - EP15 - Title.mkv",
    "Another Example - 05.mkv",
    "S02 - EP20 Jujutsu Kaisen [480p] [Sub] @Animes_Xyz.mkv",
    "Steins Gate 0 - S2 E17 [Dual] 2160p @Anime_Fair.mkv",
    "Attack On Titan - S1 E10 [Dual] 1080p @Anime_Fair.mkv",
    "S1 E04 - Chainsaw Man [Dual] 2160p @Anime_Fair.mkv",
    "Bleach - S17 E01 [Dual] 1080p @Anime_Fair.mkv",
    "High_School_DxD_S2_01_1080pDual_@Anime_Crimson@Anime_Sensei_Network.mkv"
]

for filename in filenames:
    episode_number = extract_episode_number(filename)
    print(f"Filename: {filename}, Extracted Episode Number: {episode_number}")
    

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

    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")

    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

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
    
