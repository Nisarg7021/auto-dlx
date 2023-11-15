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
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
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

        # Assuming you have access to the required variables (format_template, episode_number, file_name)
        _, file_extension = os.path.splitext(file_name)
        file_path = f"downloads/{new_file_name}"
        file = message

        ms = await message.reply("Trying to download...")
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
        user_id = int(message.chat.id)
        media = getattr(file, file.media.value)
        c_caption = await db.get_caption(message.chat.id)
        c_thumb = await db.get_thumbnail(message.chat.id)

        # ... (your existing code for caption and thumbnail handling)

        await ms.edit("Trying to upload...")
        type = file.media.document.mime_type.split("/")[0].lower()
        try:
            if type == "document":
                await bot.send_document(
                    message.chat.id,
                    document=file_path,
                    thumb=ph_path, 
                    caption=caption, 
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", ms, time.time()))
            elif type in ["video", "audio"]:
                await bot.send_video(
                    message.chat.id,
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
    else:
        await message.reply_text("Failed to extract the episode number from the file name. Please check the format.")
