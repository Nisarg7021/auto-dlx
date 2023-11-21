import math, time
from datetime import datetime
from pytz import timezone
from config import Config, Txt 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    percent = f"{current * 100 / total:.1f}%"
    speed = humanbytes((current / diff) * (total / 100))
    elapsed_time = round(diff)
    time_to_completion = round((total - current) / (current / diff))

    progress_str = "`{0}` | `{1}` | `{2}` | `{3}` | `{4}`".format(
        percent, humanbytes(current), humanbytes(total), speed, elapsed_time
    )

    try:
        await message.edit_text(
            text=(
                "{0}\n\n"
                "<b>Progress:</b> {1}\n"
                "<b>ETA:</b> {2}".format(
                    ud_type, progress_str, convert(time_to_completion)
                )
            ),
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Cancel",
                            callback_data=f"cancel_upload_{message.message_id}",
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        print(f"Error in progress_for_pyrogram: {e}")

# Usage:
ms = await message.reply("Trying to download...")
try:
    path = await client.download_media(
        message=file,
        file_name=file_path,
        progress=lambda current, total: progress_for_pyrogram(
            current, total, "Download", ms, time.time()
        ),
    )
except Exception as e:
    return await ms.edit(str(e))
    
            

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {b.mention}"
        )
        



