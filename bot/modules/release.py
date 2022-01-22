import os
import sys
from functools import wraps
from bot import LOGGER, dispatcher
from bot import OWNER_ID, GITHUB_USER_NAME, SUDO_USERS, AUTHORIZED_CHATS, GITHUB_TOKEN, GITHUB_DUMPER_REPO_NAME, TELEGRAM_CHANNEL_NAME, DUMPER_REPO_WORKFLOW_URL, GITHUB_USER_EMAIL, dispatcher, DB_URI
from telegram import ParseMode, Update
from telegram.ext import Updater, CallbackContext, CommandHandler, ConversationHandler, Filters
from telegram.ext.dispatcher import run_async
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage
import asyncio
from bot import bot
#from pyromod import listen
from asyncio.exceptions import TimeoutError
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)

API_TEXT = """Hi, {}.
This is Pyrogram's String Session Generator Bot. I will generate String Session of your Telegram Account.
By @Discovery_Updates
Now send your `API_ID` same as `APP_ID` to Start Generating Session."""
HASH_TEXT = "Now send your `API_HASH`.\n\nPress /cancel to Cancel Task."
PHONE_NUMBER_TEXT = (
    "Now send your Telegram account's Phone number in International Format. \n"
    "Including Country code. Example: **+14154566376**\n\n"
    "Press /cancel to Cancel Task."
)

async def release(update: Update, context: CallbackContext):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    CHAT_ID=message.chat_id
    print(CHAT_ID)
    if len(cmd) == 1:
        message.reply_text('Please Provide a Direct Link to an Android Dump')
        return
    cmd = cmd[1]



release_handler = CommandHandler(['rel', 'release'], release,
                    filters=CustomFilters.owner_filter | CustomFilters.authorized_user | CustomFilters.sudo_user, run_async=True)

dispatcher.add_handler(release_handler)
