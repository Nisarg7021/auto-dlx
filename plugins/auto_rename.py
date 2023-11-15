import re
from pyrogram import Client, filters
from helper.database import db

def extract_episode_number(filename):
    # Pattern 1: S1E01 or S01E01
    pattern1 = re.compile(r'S(\d+)E(\d+)')
    
    # Pattern 2: S02 E01
    pattern2 = re.compile(r'S(\d+) E(\d+)')
    
    # Pattern 3: Episode Number After "E" or "-"
    pattern3 = re.compile(r'[E|-](\d+)')
    
    # Pattern 4: Standalone Episode Number
    pattern4 = re.compile(r'(\d+)')
    
    # Try each pattern in order
    for pattern in [pattern1, pattern2, pattern3, pattern4]:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)  # Extracted episode number
    
    # Return None if no pattern matches
    return None

# Example Usage:
filename = "One Piece S1-07 [720p][Dual] @Anime_Edge.mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

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
    print(f"Original File Name: {file_name}")

    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")

    if episode_number:
        # Use the episode_number and format_template string to generate the new file name
        new_file_name = format_template.format(episode=episode_number)
        await message.reply_text(f"File renamed successfully to: {new_file_name}")
    else:
        await message.reply_text("Failed to extract the episode number from the file name. Please check the format.")
