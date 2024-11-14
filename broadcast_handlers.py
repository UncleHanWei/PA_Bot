from telegram import Update
from telegram.ext import ContextTypes
import os
from time import sleep
from global_variables import (
    user_status, playStatus, isPlaying, player,
)
from gtts import gTTS

# broadcast message
def broadcasting(msg) :
    global player
    global playStatus
    print('Broadcasting', msg)
    language = 'zh'
    sound_file = gTTS(text=msg, lang=language, slow=False) 
    sound_file.save("output.mp3") 
    # if broadcast while playing music
    # music will pause
    if isPlaying :
        playStatus = 'pause'
        player.pause()
        os.system("cvlc --play-and-exit output.mp3")
        player.pause()
        sleep(1)
        playStatus = 'play'
    else :
        os.system("cvlc --play-and-exit output.mp3")
    return


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None :
    global user_status
    user_status[update.effective_user.username] = 'broadcast'
    await update.message.reply_text('請輸入要廣播的訊息')
