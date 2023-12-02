import Client, filters
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

 # Define patterns with re.IGNORECASE flag
pattern1 = re.compile(r'S(\d+)\s*-\s*E(\d+).*?(\bHDRIP\b)', re.IGNORECASE)
pattern = re.compile(r'S?(\d+)\s*-\s*EP?(\d+).*?\[([0-9]{3,4}p)\]', re.IGNORECASE)
pattern3 = re.compile(r'(\d+)\s*-\s*(.*?)\s*\[([0-9]{3,4}p)\]', re.IGNORECASE)
pattern4 = re.compile(r'S(\d+)\s*(?:-\s*)?(\d+).*?\[([0-9]{3,4}p)\]', re.IGNORECASE)
pattern5 = re.compile(r'\[E(\d+)\].*?\[([0-9Kk]+)\].*?(@[^.]+)', re.IGNORECASE)
pattern6 = re.compile(r'\[EP-(\d+)\].*?\[([0-9]{3,4}p)\].*?(@[^.]+)', re.IGNORECASE)
pattern7 = re.compile(r'[S0]*(\d+)E0*(\d+).*?\[([0-9]{3,4}p)\]', re.IGNORECASE)

def extract_episode_and_quality(filename):
    # Try each pattern in order
    for pattern in [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7]:
        match = re.search(pattern, filename)
        if match:
            season_number = match.group(1) if match.group(1) else "01"
            episode_number = match.group(2)
            quality = match.group(3).lower()  # Convert to lowercase for consistency

            # Print the matched pattern
            print(f"Matched Pattern: {pattern}")

            return episode_number, season_number, quality

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

    episode_number, quality, season_number = extract_episode_and_quality(file_name)
    print(f"Extracted Season Number: {season_number}")
    print(f"Extracted Episode Number: {episode_number}")
    print(f"Extracted Quality: {quality}")

    if episode_number or quality or season_number:
        # Use season_number in the format template
        new_file_name = format_template.format(episode=episode_number, season=season_number, quality=quality)
        
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
