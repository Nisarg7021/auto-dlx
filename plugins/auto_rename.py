import re
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from helper.database import db



def extract_info_from_file(file_name):
    pattern = r'\[(.*?)\]\s*(.*?)\s*[Ss](\d+)\s*-\s*[Ee](\d+)\s*(\d+p)?\s*\[([^\]]+)\]\s*@(.*)\.mkv'
    match = re.match(pattern, file_name)

    if match:
        series_title = match.group(2)
        season_number = match.group(3)
        episode_number = match.group(4)
        quality = match.group(5) if match.group(5) else "N/A"
        subtitle = match.group(6)
        source_group = match.group(7)

        extracted_info = {
            "Series Title": series_title,
            "Season Number": season_number,
            "Episode Number": episode_number,
            "Quality": quality,
            "Subtitle": subtitle,
            "Source/Group": source_group,
        }

        return extracted_info
    else:
        return None

# Example Usage
file_name = "[AV] Jujutsu Kaisen S02 - E15 [Sub] [480p] @Animes_Vault.mkv"
info = extract_info_from_file(file_name)
print(info)

# Assuming you have a command handler in Pyrogram
@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")


# Inside the handler for file uploads
@Client.on_message(filters.private & (filters.document | filters.video))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)

    if not format_template:
        return await message.reply_text("Please set an auto rename format first using /autorename")

    # Extract information from the incoming file name
    file_name = message.document.file_name
    extracted_info = extract_info_from_file(file_name)

    if extracted_info:
        # Use the extracted_info dictionary and format_template string to generate the new file name
        new_file_name = format_template.format(
            series=extracted_info["Series Title"],
            season=extracted_info["Season Number"],
            episode=extracted_info["Episode Number"],
            quality=extracted_info["Quality"],
            subtitle=extracted_info["Subtitle"],
            source_group=extracted_info["Source/Group"],
        )

        await message.reply_text(f"File renamed successfully to: {new_file_name}")
    else:
        await message.reply_text("Failed to extract information from the file name. Please check the format.")
