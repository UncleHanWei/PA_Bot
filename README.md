# PA_Bot

本專案為 [MOLi-PA-Bot](https://github.com/NCNU-OpenSource/MOLi-PA-Bot) 的更新版本
由於套件和程式架構的各種問題，因此另開此一新的專案來修正這些問題

Update 2024-11-14:
更新所使用的 Python 版本至 3.10
增加虛擬環境 pipenv 簡化部署和相依套件管理
更新套件，棄用 youtube_dl、pafy，改用 pytubefix
更新程式架構，將模組切分開，增加程式的易讀性和維護性

## Bot_id
@MOLi_PA_bot

## 關於
為了解決和朋友在一起聽音樂，但又只有一個音響時，要不停換人連上音響播放的困擾，便用 RaspberryPi + Telegram bot 建立了一個點歌機器人。

利用 RaspberryPi 作為 Telegram bot 的 server，並用 Telegram bot 當做操作介面，讓人能透過這個 Telegram bot 點歌來播放。

只要將 RaspberryPi 接上音響，就可以像在 KTV 一樣不斷點歌，歌曲也會依序播放，如此一來便解決了更換連線設備的問題。
除此之外，機器人也提供各種播放音樂相關的操作(pause, stop、skip、volume control)讓播放音樂更輕鬆。

機器人也提供廣播功能，可以傳送文字給機器人，並在音響廣播出文字內容。
搭配 Telegram 的排程訊息功能，甚至可以達到鬧鐘或要事提醒的功能。

## 安裝
如果你也想建立自己的廣播機器人，請參照如下步驟
1. 建立機器人
    - [教學:Telegram Bot (1) 懶得自己做的事就交給機器人吧](https://z3388638.medium.com/telegram-bot-1-%E6%87%B6%E5%BE%97%E8%87%AA%E5%B7%B1%E5%81%9A%E7%9A%84%E4%BA%8B%E5%B0%B1%E4%BA%A4%E7%B5%A6%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%90%A7-c59004dc6c7b)
    - 這篇教學所使用的程式語言為 JavaScript，而本專案使用之程式語言為 Python，因此就本專案而言，實作部分會與教學略有不同，故請參考建立機器人的部分即可。
2. 準備硬體
    - 本專案需要使用樹梅派作為 Telegram bot 的 serve，因此你需要一塊樹梅派。
        - (本專案所使用的規格為 RaspberryPi 3 B+)
    - 你還需要一個音響，連接到樹梅派上，讓機器人能播放音樂。
3. 下載程式碼
    - `git clone https://github.com/UncleHanWei/PA_Bot.git`
4. Dependencies
    - 要運作此專案，需要安裝如下的套件。
    - `pipenv`
        - `pip3 install pipenv`
    - other dependencies
        - 於專案路徑下輸入以下指令
        - `pipenv install`
5. 建立 TOKEN 檔案
    - 把機器人的 TOKEN 寫入 .env 中，以便程式和機器人做連接。
6. 啟動程式
    - 做好前置作業之後，便可以啟動程式測試機器人是否能運作了。
    - 由於使用了 `pipenv`，因此執行程式的指令需要稍微更改
    - Windows: `pipenv run python bot.py`
    - Ubuntu/RaspberryPi: `pipenv run python3 bot.py`
7. 設定成 systemd 代管的服務
    - 將 `PA_Bot.service` 放進 `/etc/systemd/system` 中
    - 下指令: `sudo systemctl enable PA_Bot.service`
    - 下指令: `sudo systemctl daemon-reload`
    - 下指令: `sudo systemctl start PA_Bot.service`
    - 下指令: `sudo systemctl status PA_Bot.service`
    - 檢查運作狀態，若是正常運作就沒有問題了
