from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from helper.database import db
from config import Config

Config.USER_REPLY_TEXT = USER_REPLY_TXT

@Client.on_message(filters.private & filters.command("autorename") & filters.user(Config.ADMIN))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    # Extract the format from the command
    format_template = message.text.split("/autorename", 1)[1].strip()

    # Save the format template to the database
    await db.set_format_template(user_id, format_template)

    await message.reply_text("Auto rename format updated successfully!")

@Client.on_message(filters.private & filters.command("setmedia") & filters.user(Config.ADMIN))
async def set_media_command(client, message):    
    user_id = message.from_user.id    
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()

    # Save the preferred media type to the database
    await db.set_media_preference(user_id, media_type)

    await message.reply_text(f"Media preference set to: {media_type}")

@Client.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TXT:
        await message.reply(USER_REPLY_TXT)
