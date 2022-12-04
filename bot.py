from dotenv import load_dotenv
import os, threading
from time import sleep

import pafy, vlc
from youtube_search import YoutubeSearch
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
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

def showPlayList() :
    global isPlaying, nowPlayingSong, playList
    show_str = ''
    if isPlaying :
        show_str += 'Now Playing\n==========\n' + nowPlayingSong['title'] + '(Ordered By ' + nowPlayingSong['orderUser'] + ')\n\n'
    show_str += 'Next\n==========\n '
    if len(playList) > 0 :
        for i in range(len(playList)) :
            show_str += str(i + 1) + '. ' + playList[i]['title'] + ' (Ordered By ' + playList[i]['orderUser'] + ')\n'
        show_str += '\n'
    else :
        show_str += 'No Playlist!'
    return show_str

def show(update: Update, context: CallbackContext) -> None :
    update.message.reply_text(showPlayList())

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

def add(update: Update, context: CallbackContext) -> None :
    global user_status
    user_status[update.effective_user.username] = 'add'
    update.message.reply_text('請輸入要點的歌的關鍵字')

# play song
def playMusic(msg) :
    global player, playStatus, volume
    url = "https://www.youtube.com" + msg
    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url
    Instance = vlc.Instance("prefer-insecure")
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    volume = 60
    player.audio_set_volume(volume)
    player.play()
    sleep(5)
    playStatus = 'play'
    while playStatus != 'stop' and (player.is_playing() == 1 or playStatus == 'pause') :
        sleep(0.5)
    player.stop()
    playStatus = 'stop'
    return

def to_play() :
    global isPlaying, playing_thread, nowPlayingSong, playList, stopPlayListFlag
    while len(playList) > 0 and not stopPlayListFlag:
        nowPlayingSong = playList.pop(0)
        print('Now Playing =', nowPlayingSong['title'])
        playMusic(nowPlayingSong['url_suffix'])
    stopPlayListFlag = False
    isPlaying = False
    playing_thread = None
    return

def play(update: Update, context: CallbackContext) -> None :
    global playing_thread, isPlaying
    if len(playList) == 0 :
        update.message.reply_text("請先點歌")
    else :
        if playing_thread != None :
            if playing_thread.is_alive() :
                update.message.reply_text("It's already playing now")
        else :
            playing_thread = threading.Thread(target=to_play, args=())
            playing_thread.start()
            isPlaying = True
            update.message.reply_text(showPlayList())

def pause(update: Update, context: CallbackContext) -> None :
    global playing_thread, isPlaying, player, playStatus
    if isPlaying :
        if playStatus != 'pause' :
            playStatus = 'pause'
            player.pause()
        else :
            player.pause()
            sleep(3)
            playStatus = 'play'

def skip(update: Update, context: CallbackContext) -> None :
    global player, isPlaying
    if isPlaying :
        player.stop()

def stop(update: Update, context: CallbackContext) -> None :
    global stopPlayListFlag, playStatus
    if playing_thread != None :
        if playing_thread.is_alive() :
            playStatus = 'stop'
            stopPlayListFlag = True
            update.message.reply_text('Stopped')

def vol_up(update: Update, context: CallbackContext) -> None :
    global player, volume
    if player != None :
        volUp = volume + 5
        player.audio_set_volume(volUp)
        volume += 5
        update.message.reply_text('Volumn:' + str(volume))

def vol_down(update: Update, context: CallbackContext) -> None :
    global player, volume
    if player != None :
        volDown = volume - 5
        player.audio_set_volume(volDown)
        volume -= 5
        update.message.reply_text('Volumn:' + str(volume))


def broadcast(update: Update, context: CallbackContext) -> None :
    global user_status
    user_status[update.effective_user.username] = 'broadcast'
    update.message.reply_text('請輸入要廣播的訊息')

def button(update: Update, context: CallbackContext) -> None :
    global user_status, playList, user
    username = update.effective_user.username
    query = update.callback_query
    if username in user_status :
        search_result = user_status[username]
        addSong = search_result[int(query.data)]
        addSong['orderUser'] = '@' + username
        playList.append(addSong)
        query.edit_message_text(text="點播: {}".format(addSong['title']))
        update.callback_query.message.reply_text(showPlayList())

    user_status[username] = None

def msg(update: Update, context: CallbackContext) :
    global user_status
    username = update.effective_user.username
    msg = update.message.text
    if username in user_status :
        if user_status[username] == 'add' :
            update.message.reply_text('搜尋中...')
            result = search(msg)
            # 把搜尋的結果放到 user_status 裡面，方便後續的操作
            user_status[username] = result
            songList = []
            for i in range(len(result)) :
                songList.append(
                    [InlineKeyboardButton(text=str(i + 1)+'. ' + result[i]['title'], callback_data=i)]
                )
            sleep(1)
            update.message.reply_text('搜尋結果', reply_markup=InlineKeyboardMarkup(songList))
        elif user_status[username] == 'broadcast' :
            update.message.reply_text('broadcasting...')
            broadcasting(msg)
            update.message.reply_text('broadcast over')
            user_status[username] = None


def start(update: Update, context: CallbackContext) -> None :
    keyboard = [
        [KeyboardButton(text='/add'), KeyboardButton(text='/play'), KeyboardButton(text='/pause'), KeyboardButton(text='/skip'), KeyboardButton(text='/stop')],
        [KeyboardButton(text='/vol_down'), KeyboardButton(text='/show'), KeyboardButton(text='/vol_up')],
        [KeyboardButton(text='/broadcast')],
        [KeyboardButton(text='/start')]
    ]
    update.message.reply_text('歡迎使用 PA 機器人', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))

user_status = dict()
playStatus = 'stop'
isPlaying = False
playList = []
playing_thread = None
stopPlayListFlag = False
player = None
volume = 0

if __name__ == "__main__" :
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('show', show))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('play', play))
    updater.dispatcher.add_handler(CommandHandler('pause', pause))
    updater.dispatcher.add_handler(CommandHandler('skip', skip))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(CommandHandler('vol_up', vol_up))
    updater.dispatcher.add_handler(CommandHandler('vol_down', vol_down))
    updater.dispatcher.add_handler(CommandHandler('broadcast', broadcast))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(~Filters.command, msg))

    updater.start_polling()
    print('bot start listening...')
    updater.idle()