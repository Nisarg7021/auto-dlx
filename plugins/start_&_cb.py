"""
Apache License 2.0
Copyright (c) 2022 @PYRO_BOTZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/PYRO_BOTZ 
Repo Link : https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT
License Link : https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT/blob/main/LICENSE
"""

import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message, InputMediaPhoto

from helper.database import db
from config import Config, Txt  

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)                
    button = InlineKeyboardMarkup([[
      InlineKeyboardButton("⚡ 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 ⚡", callback_data='commands')
    ],[
      InlineKeyboardButton('Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/Nation_Bots'),
      InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url='https://t.me/Nation_Support')
    ],[
      InlineKeyboardButton('Hᴇʟᴘ', callback_data='about'),
      InlineKeyboardButton('Pʀᴇᴍɪᴜᴍ', callback_data='premium')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)   

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    user_id = query.from_user.id  # Fix here
    
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⚡ 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 ⚡", callback_data='commands')
                ],[
                InlineKeyboardButton('Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/Nation_Bots'),
                InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url='https://t.me/Nation_Support')
                ],[
                InlineKeyboardButton('Hᴇʟᴘ', callback_data='about'),
                InlineKeyboardButton('Pʀᴇᴍɪᴜᴍ', callback_data='premium')
            ]])
        )
    elif data == "premium":
        await query.message.edit_text(
            text=Txt.PREMIUM_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('Bᴜʏ Nᴏᴡ ⚡', url='https://t.me/Trippy_xt')
                ],[
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Sᴇᴛᴜᴘ Aᴜᴛᴏʀᴇɴᴀᴍᴇ Fᴏʀᴍᴀᴛ", callback_data='file_names')
                ],[
                InlineKeyboardButton('Tʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                InlineKeyboardButton('Sᴇǫᴜᴇɴᴄᴇ', url='https://t.me/File_Sequencer_Bot')
                ],[
                InlineKeyboardButton('Pʀᴇᴍɪᴜᴍ', callback_data='premium'),
                InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about')
                ],[
                InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start')
            ]])
        )
    elif data == "commands":
        await query.message.edit_text(
            text=Txt.COMMANDS_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="start")
            ]])          
        )
    
    elif data == "file_names":
        format_template = await db.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about")
            ]])
        )      
    
    elif data == "thumbnail":
        user_thumbnail = await db.get_thumbnail(user_id)
        
    # Edit the message to show text and buttons
        await query.message.edit_text(
            text=Txt.THUMB_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about"),
            ]]),
        )
        
    # If the user has set a custom thumbnail, edit the message to replace the photo
        if user_thumbnail:
            await query.message.edit_media(
                media=InputMediaPhoto(user_thumbnail),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                    InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about"),
                ]]),
            )
        else:
            await query.message.reply_photo(Config.START_PIC)
        
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
