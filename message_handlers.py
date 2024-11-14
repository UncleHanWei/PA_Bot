from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from broadcast_handlers import broadcasting
from global_variables import user_status
from youtube_search import YoutubeSearch

def search(msg) :
    results = YoutubeSearch(msg, max_results=15).to_dict()
    new_results = []
    count = 0
    for i in range(len(results)) :
        if results[i]['duration'] == 0 :
            continue
        if count == 10 :
            break
        results[i]['url_suffix'] = results[i]['url_suffix'].replace('shorts/', 'watch?v=')
        new_results.append(results[i])
        count += 1
    return new_results


async def handle_add(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    username = update.effective_user.username
    msg = update.message.text
    result = search(msg)
    # 把搜尋的結果放到 user_status 裡面，方便後續的操作
    user_status[username] = result
    songList = []
    for i in range(len(result)) :
        songList.append(
            [InlineKeyboardButton(text=str(i + 1)+'. ' + result[i]['title'], callback_data=i)]
        )
    await update.message.reply_text('搜尋結果', reply_markup=InlineKeyboardMarkup(songList))


async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    username = update.effective_user.username
    msg = update.message.text
    await update.message.reply_text('broadcasting...')
    broadcasting(msg)
    await update.message.reply_text('broadcast over')
    user_status[username] = None


async def handle_default(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    return


async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    handle_func_map = {
        "add": handle_add,
        "broadcast": handle_broadcast,
        "default": handle_default,
    }
    username = update.effective_user.username

    # 取得使用者當前的指令狀態，如果沒有就是 default
    cur_user_status = user_status.get(username, 'default')
    await handle_func_map[cur_user_status](update, context)