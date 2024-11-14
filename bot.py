from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder,
    CommandHandler, CallbackQueryHandler
)
from dotenv import dotenv_values

from basic_handlers import start
from message_handlers import msg
from music_handlers import (
    show, add, play, pause,
    skip, stop, vol_up, vol_down
)
from broadcast_handlers import broadcast
from callback_query_handlers import button

def main() :
    config = dotenv_values(".env")
    app = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

    # set handlers
    # basic handler
    app.add_handler(CommandHandler('start', start))

    # message handler
    app.add_handler(MessageHandler(~filters.COMMAND, msg))

    # music handler
    app.add_handler(CommandHandler('show', show))
    app.add_handler(CommandHandler('add', add))
    app.add_handler(CommandHandler('play', play))
    app.add_handler(CommandHandler('pause', pause))
    app.add_handler(CommandHandler('skip', skip))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('vol_up', vol_up))
    app.add_handler(CommandHandler('vol_down', vol_down))

    # callback broadcast handler
    app.add_handler(CommandHandler('broadcast', broadcast))

    # callback query handler
    app.add_handler(CallbackQueryHandler(button))

    print("Bot start listening...")
    app.run_polling()


if __name__ == "__main__" :
    try :
        print("Build bot instance...")
        main()
    finally :
        print("Bot stopped.")
