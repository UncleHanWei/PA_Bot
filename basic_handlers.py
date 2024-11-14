from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None :
    reply_str = '歡迎使用 PA 機器人'
    keyboard = [
        [KeyboardButton(text='/add'), KeyboardButton(text='/play'), KeyboardButton(text='/pause'), KeyboardButton(text='/skip'), KeyboardButton(text='/stop')],
        [KeyboardButton(text='/vol_down'), KeyboardButton(text='/show'), KeyboardButton(text='/vol_up')],
        [KeyboardButton(text='/broadcast')],
        [KeyboardButton(text='/start')]
    ]
    await update.message.reply_text(reply_str, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))
