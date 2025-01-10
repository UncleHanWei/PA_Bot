from telegram import Update
from telegram.ext import ContextTypes
from time import sleep
from global_variables import (
    user_status, playStatus, isPlaying, playList,
    playing_thread, player, volume, stopCmd
)
from pytubefix import YouTube, exceptions
import vlc
import threading


def showPlayList() :
    global isPlaying, nowPlayingSong, playList
    show_str = ''
    if isPlaying :
        show_str += 'Now Playing\n==========\n' + nowPlayingSong['title'] + '(Ordered By ' + nowPlayingSong['orderUser'] + ') \n\n'
    show_str += 'Next\n==========\n '
    if len(playList) > 0 :
        for i in range(len(playList)) :
            show_str += str(i + 1) + '. ' + playList[i]['title'] + ' (Ordered By ' + playList[i]['orderUser'] + ')\n'
        show_str += '\n'
    else :
        show_str += 'No Playlist!'
    return show_str


def to_play() :
    global isPlaying, playing_thread, nowPlayingSong, playList, stopCmd
    while len(playList) > 0 and not stopCmd:
        nowPlayingSong = playList.pop(0)
        print('Now Playing =', nowPlayingSong['title'])
        playMusic(nowPlayingSong['url_suffix'])
    stopCmd = False
    isPlaying = False
    playing_thread = None
    return


async def show(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text(showPlayList())



async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None :
    global user_status
    user_status[update.effective_user.username] = 'add'
    await update.message.reply_text('請輸入要點的歌的關鍵字')


# play song
def playMusic(msg) :
    global player, playStatus, volume
    try :
        url = "https://www.youtube.com" + msg
        yt = YouTube(url.strip())
        stream = yt.streams.filter(only_audio=True).first()
        stream_url = stream.url
        instance = vlc.Instance("prefer-insecure")
        player = instance.media_player_new()
        media = instance.media_new(stream_url)
        player.set_media(media)
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
    except exceptions.AgeRestrictedError :
        print("AgeRestrictedError")
    except Exception :
        print("Exception")
    finally :
        return


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global playing_thread, isPlaying
    if len(playList) == 0 :
        await update.message.reply_text("請先點歌")
    else :
        if playing_thread != None :
            if playing_thread.is_alive() :
                await update.message.reply_text("It's already playing now")
        else :
            playing_thread = threading.Thread(target=to_play, args=())
            playing_thread.start()
            isPlaying = True
            await update.message.reply_text(showPlayList())


def pause(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global playing_thread, isPlaying, player, playStatus
    if isPlaying :
        if playStatus != 'pause' :
            playStatus = 'pause'
            player.pause()
        else :
            player.pause()
            sleep(3)
            playStatus = 'play'


def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global player, isPlaying
    if isPlaying :
        player.stop()


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global stopCmd, playStatus
    if playing_thread != None :
        if playing_thread.is_alive() :
            playStatus = 'stop'
            stopCmd = True
            await update.message.reply_text('Stopped.')


async def vol_up(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global player, volume
    volUp = volume + 5
    if volUp <= 100 :
        player.audio_set_volume(volUp)
        volume += 5
        return True
    else :
        return False


async def vol_down(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global player, volume
    volDown = volume - 5
    if volDown >= 5 :
        player.audio_set_volume(volDown)
        volume -= 5
        return True
    else :
        return False
