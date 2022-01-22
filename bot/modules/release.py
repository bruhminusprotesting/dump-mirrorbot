import os
import sys
from functools import wraps
from bot import LOGGER, dispatcher
from bot import OWNER_ID, GITHUB_USER_NAME, SUDO_USERS, AUTHORIZED_CHATS, GITHUB_TOKEN, GITHUB_DUMMY_REPO_NAME, TELEGRAM_CHANNEL_NAME, GITHUB_USER_EMAIL, dispatcher, DB_URI
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage

AUTHORIZED_CHATS.add(OWNER_ID)
import subprocess
import string
import random
import asyncio

from bot import bot
from pyromod import listen
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

bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile='/tmp/'+bashfile+'.sh'
#CHAT_ID = update.effective_chat.id
f = open(bashfile, 'w')
s = """#!/bin/bash
ORIGINAL_PATH=$(pwd)
ORIGINAL_GIT_USER_EMAIL=$(git config user.email)
ORIGINAL_GIT_USER_NAME=$(git config user.name)
echo "$1" | grep -e '^\(https\?\|ftp\)://.*$' > /dev/null;
CODE=$1
set -- $CODE
GITHUB_TOKEN=$1
GITHUB_USER_NAME=$2
GITHUB_REPO_NAME=$3
GITHUB_USER_EMAIL=$4
TELEGRAM_CHANNEL_NAME=$5
CURRENT_CHAT_ID=$6
URL=$7
BRANCH=$8
URL_WITHOUT_HTTPS=$(echo "$URL" |sed 's/https\?:\/\///')
NEW_URL=https://${GITHUB_USER_NAME}:${GITHUB_TOKEN}@${URL_WITHOUT_HTTPS} #just incase its a dump from own private org
DUMP_NAME=$(echo $URL_WITHOUT_HTTPS | sed 's/.*\///')
git config --global user.email "$GITHUB_USER_EMAIL"
git config --global user.name "$GITHUB_USER_NAME"
git config --global credential.helper cache  
git ls-remote "$NEW_URL" > /dev/null 2>&1
if [ "$?" -ne 0 ]; then echo "[ERROR] "$NEW_URL" is not a git repo" && exit 1; fi
git clone --depth=1 --single-branch --quiet https://${GITHUB_USER_NAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USER_NAME}/${GITHUB_REPO_NAME} ~/tempdirectorysirbro
cd ~/tempdirectorysirbro
rm -rf BRANCH.txt URL.txt CURRENT_CHAT_ID.txt
echo "$CURRENT_CHAT_ID" > CURRENT_CHAT_ID.txt
echo "${URL}" > URL.txt
if [[ "${BRANCH}" == "" ]] ; then touch BRANCH.txt ; else echo "${BRANCH}" > BRANCH.txt && git add BRANCH.txt ; fi
git add URL.txt CURRENT_CHAT_ID.txt
git commit -m "Generate Dummy Tree Using $DUMP_NAME"
git push -f --quiet https://${GITHUB_USER_NAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USER_NAME}/${GITHUB_REPO_NAME}
cd ${ORIGINAL_PATH}
rm -rf ${GITHUB_REPO_NAME}
git config --global user.email "$ORIGINAL_GIT_USER_EMAIL"
git config --global user.name "$ORIGINAL_GIT_USER_NAME"
"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd=bashfile
for arg in sys.argv[1:]:
  bashcmd += ' '+arg

@bot.on_message(filters.private & filters.command("release"))
async def genStr(_, msg: Message):
    chat = msg.chat
    api = await bot.ask(
        chat.id, API_TEXT.format(msg.from_user.mention)
    )
    if await is_cancel(msg, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await msg.reply("`API_ID` is Invalid.\nPress /start to Start again.")
        return
    api_id = api.text
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    if not len(hash.text) >= 30:
        await msg.reply("`API_HASH` is Invalid.\nPress /start to Start again.")
        return
    api_hash = hash.text
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`Is "{phone}" correct? (y/n):` \n\nSend: `y` (If Yes)\nSend: `n` (If No)')
        if await is_cancel(msg, confirm.text):
            return
        if "y" in confirm.text:
            break
    try:
        client = Client("my_account", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait as e:
        await msg.reply(f"You have Floodwait of {e.x} Seconds")
        return
    except ApiIdInvalid:
        await msg.reply("API ID and API Hash are Invalid.\n\nPress /start to Start again.")
        return
    except PhoneNumberInvalid:
        await msg.reply("Your Phone Number is Invalid.\n\nPress /start to Start again.")
        return
    try:
        otp = await bot.ask(
            chat.id, ("An OTP is sent to your phone number, "
                      "Please enter OTP in `1 2 3 4 5` format. __(Space between each numbers!)__ \n\n"
                      "If Bot not sending OTP then try /restart and Start Task again with /start command to Bot.\n"
                      "Press /cancel to Cancel."), timeout=300)

    except TimeoutError:
        await msg.reply("Time limit reached of 5 min.\nPress /start to Start again.")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await msg.reply("Invalid Code.\n\nPress /start to Start again.")
        return
    except PhoneCodeExpired:
        await msg.reply("Code is Expired.\n\nPress /start to Start again.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "Your account have Two-Step Verification.\nPlease enter your Password.\n\nPress /cancel to Cancel.",
                timeout=300
            )
        except TimeoutError:
            await msg.reply("`Time limit reached of 5 min.\n\nPress /start to Start again.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await client.send_message("me", f"#PYROGRAM #STRING_SESSION\n\n```{session_string}``` \n\nBy [@StringSessionGen_Bot](tg://openmessage?user_id=1472531255) \nA Bot By @Discovery_Updates")
        await client.disconnect()
        text = "String Session is Successfully Generated.\nClick on Below Button."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Show String Session", url=f"tg://openmessage?user_id={chat.id}")]]
        )
        await bot.send_message(chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
