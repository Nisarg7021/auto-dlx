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

import re, os, time

id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "23374527")
    API_HASH  = os.environ.get("API_HASH", "5a48ec466dfa7df47e2a109ed40019bc")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6476477100:AAFyDA7J7y6lEutSwPUEuz9JzW54tn_HjsA") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","pyro-botz")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://dlxsmith:8876790388@cluster0.jfy5pyy.mongodb.net/?retryWrites=true&w=majority")
    
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/a58a94d97b5f7a82d44c4.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1951547289 1747003935 6446763201 5173665421 1785499774').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002068600193"))
    FILES_CHANNEL = int(os.environ.get("FILES_CHANNEL", "-1001999057119"))
    USER_REPLY_TEXT = "Your Are Not Authorised To use me Contact @dlx_smith to use me "

    
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):
    # part of text configuration
        
    START_TXT = """<b>Hɪ {} 👋,
Tʜɪs Is Aɴ Aᴅᴠᴀɴᴄᴇᴅ Aɴᴅ Yᴇᴛ Pᴏᴡᴇʀꜰᴜʟ Rᴇɴᴀᴍᴇ Bᴏᴛ
Usɪɴɢ Tʜɪs Bᴏᴛ Yᴏᴜ Cᴀɴ Rᴇɴᴀᴍᴇ & Cʜᴀɴɢᴇ Tʜᴜᴍʙɴᴀɪʟ Oꜰ Yᴏᴜʀ Fɪʟᴇ
Yᴏᴜ Cᴀɴ Aʟsᴏ Cᴏɴᴠᴇʀᴛ Vɪᴅᴇᴏ Tᴏ Fɪʟᴇ & Fɪʟᴇ Tᴏ Vɪᴅᴇᴏ
Tʜɪs Bᴏᴛ Aʟꜱᴏ Sᴜᴘᴘᴏʀᴛs Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ Aɴᴅ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ
Tʜɪs Bᴏᴛ Wᴀs Cʀᴇᴀᴛᴇᴅ Bʏ : @Nation_Bots ⚡</b>"""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>\n\nUse These Keywords To Setup Custom File Name\n\n➝ episode :- to replace episode number\n➝ quality :- to replace video resolution\n\n‣ <b>Example :</b> /autorename [AX] S02 - EPepisode Spy X Family [quality] [Sub] @Animes_XYZ.mkv\n\n‣ <b>Your Current Rename Format :</b> {format_template}
    """
    
    ABOUT_TXT = f"""
<b>╔════════════⦿
├⋗ ᴄʀᴇᴀᴛᴏʀ : <a href='tg://user?id={1785499774}'>Dlx Smith</a>
├⋗ ʟᴀɴɢᴜᴀɢᴇ : <code>Python3</code>
├⋗ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pyrogram</a>
├⋗ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : <a href='https://t.me/Trippy_xd/2'>Click Here</a>
├⋗ Main Channel : <a href='https://t.me/animes_in_30mb'>Anime Channel</a>
├⋗ Support Group : <a href='https://t.me/Animetalks0'>Group Chat</a>
╚═════════════════⦿</b>
"""

    
    THUMB_TXT = """ᴛᴏ ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ
➜ /start: ꜱᴇɴᴅ ᴀɴʏ ᴘʜᴏᴛᴏ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ꜱᴇᴛ ɪᴛ ᴀꜱ ᴀ ᴛʜᴜᴍʙɴᴀɪʟ..
➜ /del_thumb: ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏʟᴅ ᴛʜᴜᴍʙɴᴀɪʟ.
➜ /view_thumb: ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ.
ɴᴏᴛᴇ: ɪꜰ ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴀᴠᴇᴅ ɪɴ ʙᴏᴛ ᴛʜᴇɴ, ɪᴛ ᴡɪʟʟ ᴜꜱᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ᴛʜᴇ ᴏʀɪɢɪɴɪᴀʟ ꜰɪʟᴇ ᴛᴏ ꜱᴇᴛ ɪɴ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇ"""
    

    PREMIUM_TXT = """✨ Pʀᴇᴍɪᴜᴍ Bᴇɴᴇғɪᴛs ✨

Uᴘɢʀᴀᴅᴇ ᴛᴏ ᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ᴇɴJᴏʏ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs:
➲ Uɴʟɪᴍɪᴛᴇᴅ Rᴇɴᴀᴍɪɴɢ: ʀᴇɴᴀᴍᴇ ᴀs ᴍᴀɴʏ ғɪʟᴇs ᴀs ʏᴏᴜ ᴡᴀɴᴛ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ʀᴇsᴛʀɪᴄᴛɪᴏɴs.
➲ Eᴀʀʟʏ Aᴄᴄᴇss: ʙᴇ ᴛʜᴇ ғɪʀsᴛ ᴛᴏ ᴛᴇsᴛ ᴀɴᴅ ᴜsᴇ ᴏᴜʀ ʟᴀᴛᴇsᴛ ғᴇᴀᴛᴜʀᴇs ʙᴇғᴏʀᴇ ᴀɴʏᴏɴᴇ ᴇʟsᴇ.

Pʀɪᴄɪɴɢ:
➜ Contact:- @Dlx_smith

Uɴʟᴏᴄᴋ ᴛʜᴇ ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ ᴏғ ᴏᴜʀ ʀᴇɴᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss. Sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴀɴᴅ sᴜᴘᴇʀᴄʜᴀʀɢᴇ ʏᴏᴜʀ ғɪʟᴇ ʀᴇɴᴀᴍɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ! ⚡️

Tᴏ sᴜʙsᴄʀɪʙᴇ, sɪᴍᴘʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴏᴜʀ ᴅᴇᴠᴇʟᴏᴘᴇʀ ʙᴇʟᴏᴡ."""


    COMMANDS_TXT = """<b>✨Auto Rename Bot🫧
 ʙᴏᴛ ɪꜱ ᴀ ʜᴀɴᴅʏ ᴛᴏᴏʟ ᴛʜᴀᴛ ʜᴇʟᴘꜱ ʏᴏᴜ ᴛᴏ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ʙʏ ɢɪᴠɪɴɢ ᴄᴏᴍᴍᴀɴᴅ /Aᴜᴛᴏʀᴇɴᴀᴍᴇ [Yᴏᴜʀ ғᴏʀᴍᴀᴛ] ᴀɴᴅ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ꜰɪʟᴇꜱ ᴇꜰꜰᴏʀᴛʟᴇꜱꜱʟʏ.
ɪᴍᴘᴏʀᴛᴀɴᴛ ᴄᴏᴍᴍᴀɴᴅꜱ:
➲ /Autorename: ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ꜰɪʟᴇꜱ.
➲ /View_Thumb: ᴛᴏ sᴇᴇ ᴄᴏᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ.
➲ /Setmedia: sᴇᴛ ʏᴏᴜʀ ᴜᴘʟᴏᴀᴅ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ."""

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""
