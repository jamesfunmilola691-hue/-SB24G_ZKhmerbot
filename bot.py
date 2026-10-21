import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# This line tells Railway to look for the TOKEN in the Variables tab
TOKEN = os.environ.get("TOKEN", "YOUR_BOT_TOKEN_HERE")
