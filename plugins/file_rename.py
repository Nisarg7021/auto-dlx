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

def extract_episode_number(filename):
    # Define regular expressions for each piece of information
    season_pattern = re.compile(r'S(\d+)', re.IGNORECASE)
    episode_pattern = re.compile(r'E(\d+)|EP(\d+)|(\d+)', re.IGNORECASE)
    title_pattern = re.compile(r'[\[\(](.*?)[\]\)]', re.IGNORECASE)
    audio_pattern = re.compile(r'Dual|Su', re.IGNORECASE)
    quality_pattern = re.compile(r'1080p|720p|2k|4k|2160p|480p', re.IGNORECASE)
    channel_pattern = re.compile(r'@(\w+)', re.IGNORECASE)
    extension_pattern = re.compile(r'\.(mkv|mp4|mp3)', re.IGNORECASE)

    # Initialize variables to store extracted information
    season = episode = title = audio = quality = channel = extension = None

    # Search for patterns in the filename
    season_match = re.search(season_pattern, filename)
    episode_match = re.search(episode_pattern, filename)
    title_match = re.search(title_pattern, filename)
    audio_match = re.search(audio_pattern, filename)
    quality_match = re.search(quality_pattern, filename)
    channel_match = re.search(channel_pattern, filename)
    extension_match = re.search(extension_pattern, filename)

    # Extract information if a match is found
    if season_match:
        season = season_match.group(1)
    if episode_match:
        episode = next(x for x in episode_match.groups() if x)
    if title_match:
        title = title_match.group(1)
    if audio_match:
        audio = audio_match.group(0)
    if quality_match:
        quality = quality_match.group(0)
    if channel_match:
        channel = channel_match.group(1)
    if extension_match:
        extension = extension_match.group(1)

    return {
        'season': season,
        'episode': episode,
        'title': title,
        'audio': audio,
        'quality': quality,
        'channel': channel,
        'extension': extension
    }

# Test the function with examples
filenames = [
    "S1 E03 - Chainsaw Man [Dual] 480p @Anime_Fair.mkv",
    "103 - Migration Season.nov",
    "[AC] Spy x Family S02 E08 [480p] [Sub] @Anime_Campus.mkv",
    "179 - Bleach [Dual] [480p] @Anime_Wars.mkv",
    "[HG] Jujutsu Kaisen - S2E20 [Hdrip][Sub] @HG_Anime.mkv",
    "[E10] [480p] Under Ninja [Sub] @The_NightOwls.mkv",
    "High_School_DxD_S1_04_1080pDual_@Anime_Crimson@Anime_Sensei_Network.mkv",
    "Steins Gate 0 - S2 E17 [Dual] 2160p @Anime_Fair.nov",
    "[AR] My Hero Academia S1 - 02 [720p] [Dual].mkv",
    "[S02-E12] ClassRoom of the Elite [2k] [Dual] @Anime_Alliance.mkv",
    "[@Anime_RTX] Jujutsu kaisen S2E20 [4K×264][Sub].mkv"
]

for filename in filenames:
    info = extract_episode_info(filename)
    print(f"Filename: {filename}")
    print("Extracted Info:", info)
    print("=" * 50)
    
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
    
