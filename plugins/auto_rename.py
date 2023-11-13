import re
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

from PIL import Image
import os, time

import re

def extract_episode_number(filename):
    # Updated Pattern: [AV] Undead Unluck S01 - E06 [Sub] [480p] @Animes_Vault.mkv
    pattern = re.compile(r'S(\d+)[\s-]*E(\d+)', re.IGNORECASE)
    
    match = re.search(pattern, filename)
    if match:
        season_number, episode_number = match.groups()
        return f"S{season_number}E{episode_number}"

    # Return None if no pattern matches
    return None
	

# Example Usage:
filename = "[AV] Undead Unluck S01 - E06 [Sub] [480p] @Animes_Vault.mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

# Assuming you have a command handler in Pyrogram
@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extracted the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")
	
@Client.on_message(filters.private & (filters.document | filters.video))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)

    if not format_template:
        return await message.reply_text("Please set an auto rename format first using /autorename")

    # Extract information from the incoming file name
    file_name = message.document.file_name
    print(f"Original File Name: {file_name}")

    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")
	
# Inside your auto_rename_files handler after extracting the episode number
if episode_number:
    # Use the episode_number and format_template string to generate the new file name
    new_file_name = format_template.format(episode=episode_number)
    await message.reply_text(f"File renamed successfully to: {new_file_name}")

    # Send a message with inline keyboard markup
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upload", callback_data=f"upload_{new_file_name}")]
    ])
    await bot.send_message(user_id, "Do you want to upload the file now?", reply_markup=keyboard)

    # Auto-activate the callback query "Upload"
    await bot.send_callback_query(
        chat_id=user_id,
        message_id=message.message_id + 1,  # Assuming the message_id of the previous message
        data=f"upload_{new_file_name}"
    )
else:
    await message.reply_text("Failed to extract the episode number from the file name. Please check the format.")

	
    if episode_number:
        # Use the episode_number and format_template string to generate the new file name
        new_file_name = format_template.format(episode=episode_number)
        await message.reply_text(f"File renamed successfully to: {new_file_name}")
    else:
        await message.reply_text("Failed to extract the episode number from the file name. Please check the format.")	    

# Define a callback handler for document upload
@Client.on_callback_query(filters.regex("upload"))
async def docs(bot, update):
    # Assuming you have access to the required variables (format_template, episode_number, file_name)
    new_file_name = format_template.format(episode=episode_number)
    _, file_extension = os.path.splitext(file_name)
    file_path = f"downloads/{new_file_name}"
    file = update.message.reply_to_message

    ms = await update.message.edit("Trying to download...")
    try:
        path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", ms, time.time()))
    except Exception as e:
        return await ms.edit(str(e))

    duration = 0
    try:
        duration = get_duration(file_path)
    except Exception as e:
        print(f"Error getting duration: {e}")
        duration = 0
    finally:
        pass

    ph_path = None
    user_id = int(update.message.chat.id)
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
   
    await ms.edit("Trying to upload...")
    type = update.data.split("_")[1]
    try:
        if type == "document":
            await bot.send_document(
                update.message.chat.id,
                document=file_path,
                thumb=ph_path, 
                caption=caption, 
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time()))
        elif type == "video":
            await bot.send_video(
                update.message.chat.id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time()))
    except Exception as e:
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return await ms.edit(f"Error {e}")

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)
    
