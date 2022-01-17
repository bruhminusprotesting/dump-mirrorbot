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

def release(update: Update, context: CallbackContext):
    CHAT_ID=message.chat_id
    USER_ID = f"{message.from_user.id}"
    FIRST_NAME = f"{message.from_user.first_name}"
    if message.from_user.username:
        USER_TAG = f"@{message.from_user.username}"
    else:
        USER_TAG = f"none"



release_handler = CommandHandler(BotCommands.MirrorCommand, release,
                                filters=CustomFilters.authorized_chat | CustomFilters.sudo_user | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(release_handler)