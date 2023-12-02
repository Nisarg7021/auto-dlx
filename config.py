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
    API_ID    = os.environ.get("API_ID", "22418774")
    API_HASH  = os.environ.get("API_HASH", "d8c8dab274f9a811814a6a96d044028e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6847089573:AAGMWg1OuyGNnpIQGnptDFYQVwcQcJF-oYQ") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","pyro-botz")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://mehtadmphta33:Mehtab1234@cluster0.bfsb3oq.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://telegra.ph/file/c9e6c33aad7f8526f3118.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6446763201').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002099814452"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):
    # part of text configuration
        
    START_TXT = """Hello {}

⚡ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐍𝐀𝐓𝐈𝐎𝐍'𝐒 𝐀𝐃𝐕𝐀𝐍𝐂𝐄𝐃 𝐑𝐄𝐍𝐀𝐌𝐄 𝐁𝐎𝐓! ⚡

➝  Introducing Advanced Rename Bot – your ultimate solution for effortless file renaming, featuring customizable captions, thumbnails, and seamless sequencing.
────────────────────
✨ Tʜɪs Bᴏᴛ ɪs Cʀᴇᴀᴛᴇᴅ ʙʏ <a href='https://t.me/Trippy_xt'>Tʀɪᴘᴘʏ</a>
────────────────────
➝  For assistance or more How to use me, use the " /Tutorial "command or you can use the below "Support" button to contact us.

‼️ Explore my commands by clicking on the '⚡ Commands⚡' button to use me more precisely " ‼️

🚀 𝐋𝐄𝐓'𝐒 𝐆𝐄𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃! 🚀"""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>

    Use These Keywords To Setup Custom File Name

    ➝ {episode} - to replace episode number
    ➝ {quality} - to replace video resolution 

    ‣ <b>Example :</b> /autorename [AX] S02 - EP{episode} Spy X Family [{quality}] [Sub] @Animes_XYZ.mkv

    ‣ Your Current Rename Format :</b> {format_template}
    """

    THUMB_TXT = """just send the image nigga"""
    
    ABOUT_TXT = f"""
<b>╔════════════⦿
├⋗ ᴄʀᴇᴀᴛᴏʀ : <a href='tg://user?id={6446763201}'>⚚ 𝐓𝐑𝐈𝐏𝐏𝐘 ❄️ </a>
├⋗ ʟᴀɴɢᴜᴀɢᴇ : <code>Python3</code>
├⋗ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pyrogram</a>
├⋗ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : <a href='https://t.me/Trimppy/2'>Click Here</a>
├⋗ Main Channel : <a href='https://t.me/Animes_Xyz'>Anime Channel</a>
├⋗ Support Group : <a href='https://t.me/Animetalks0'>Group Chat</a>
╚═════════════════⦿</b>
"""

    
    THUMB_TXT = """ just send the image nigga"""

    PREMIUM_TXT = """ premium ke liye rates btao guyz"""

#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @ᴩyʀᴏ_ʙᴏᴛᴢ🙏🥲
    COMMANDS_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>
    """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""


