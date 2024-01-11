# Made by @Nation_Bots

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
      InlineKeyboardButton('Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/animes_in_30mb'),
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
    user_id = query.from_user.id  
    
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⚡ 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 ⚡", callback_data='commands')
                ],[
                InlineKeyboardButton('Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/animes_in_30mb'),
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
                InlineKeyboardButton('Bᴜʏ Nᴏᴡ ⚡', url='https://t.me/Dlx_smith')
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
        
        await query.message.edit_media(
            media=InputMediaPhoto(user_thumbnail),
        )
        await query.message.edit_caption(
            caption=Txt.THUMB_TXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data="about"),
            ]]),
        )
    
    
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

# Made by @Nation_Bots

