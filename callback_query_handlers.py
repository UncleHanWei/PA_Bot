from telegram import Update
from telegram.ext import ContextTypes
from global_variables import user_status, playList
from music_handlers import showPlayList


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None :
    global user_status, playList
    username = update.effective_user.username
    query = update.callback_query
    if username in user_status :
        search_result = user_status[username]
        addSong = search_result[int(query.data)]
        addSong['orderUser'] = '@' + username
        playList.append(addSong)
        await query.edit_message_text(text="點播: {}".format(addSong['title']))
        await update.callback_query.message.reply_text(showPlayList())

    user_status.pop(username)
