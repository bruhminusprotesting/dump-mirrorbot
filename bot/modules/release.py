import os
import sys
from functools import wraps
from bot import LOGGER, dispatcher
from bot import OWNER_ID, GITHUB_USER_NAME, SUDO_USERS, AUTHORIZED_CHATS, GITHUB_TOKEN, GITHUB_DUMMY_REPO_NAME, TELEGRAM_CHANNEL_NAME, GITHUB_USER_EMAIL, dispatcher, BOT_TOKEN, DB_URI
from telegram import ParseMode, Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, Updater, MessageHandler, ConversationHandler
from telegram.ext.dispatcher import run_async
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage
AUTHORIZED_CHATS.add(OWNER_ID)
#AUTHORIZED_CHATS.add(SUDO_USERS)
import subprocess
import string
import random
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

DEVICE_CODENAME, DEVICE_NAME, OTA_STATUS, DOWNLOAD_LINK, ANDROID_VERSION, BUGS, TELEGRAPH_FLASH_STEPS_LINK, ARE_THERE_GAPPS, RECOVERY_DOWNLOAD_LINK, FIRMWARE_DOWNLOAD_LINK, BUILD_CHANGELOG, USER_NOTES, ARE_VALUES_CORRECT, PHOTO, LOCATION, BIO = range(16)

def release(update: Update, context: CallbackContext) -> str:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    #if user.id in AUTHORIZED_CHATS:
    #    print(user.id)
    #else:
    #    update.message.reply_text(
    #            "This is a temp restricted command."
    #            " You do not have permissions to run this.")
    #    stop()
    if not user.id in AUTHORIZED_CHATS:
            update.message.reply_text(
                "This is a temp restricted command."
                " You do not have permissions to run this.")
            return

    update.message.reply_text(
        "Enter Your Device Codename."
        "Use /stop to exit."
    )
    return DEVICE_CODENAME
    #return DEVICE_NAME

def device_codename(update: Update, context: CallbackContext) -> str:
    """Stores the device_codename and asks for device_name."""
    global NEW_DEVICE_CODENAME
    NEW_DEVICE_CODENAME = update.message.text.lower()
    user = update.message.from_user
    update.message.reply_text('Send Your Device Name(example: Realme C1):')
    return DEVICE_NAME

def device_name(update: Update, context: CallbackContext) -> str:
    """Stores the device_name and asks for OTA Status."""
    global NEW_DEVICE_NAME
    NEW_DEVICE_NAME = update.message.text
    user = update.message.from_user
    update.message.reply_text('Do You Want To Send an OTA Update To Users For This Build? (y/n).')
    return OTA_STATUS

def ota_status(update: Update, context: CallbackContext) -> str:
    """Stores Device Name And Asks For OTA Status."""
    global NEW_OTA_STATUS
    NEW_OTA_STATUS = update.message.text.lower()
    user = update.message.from_user
    if 'y' in NEW_OTA_STATUS:
        NEW_OTA_STATUS='y'
        update.message.reply_text('OTA Disabled For this build.')
    elif 'n' in NEW_OTA_STATUS:
        NEW_OTA_STATUS='y'
        update.message.reply_text('OTA Disabled For this build.')
    else:
        update.message.reply_text('Invalid Input. Enter Either \'y\' or \'n\'')
        return OTA_STATUS
    update.message.reply_text('Provide A Direct Download Link To Your Build.')
    return DOWNLOAD_LINK

def download_link(update: Update, context: CallbackContext) -> int:
    """Stores OTA Info and asks for download link."""
    global NEW_DOWNLOAD_LINK
    NEW_DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    if 'http' in NEW_DOWNLOAD_LINK:
        update.message.reply_text('What\'s the android version?(integer values only).')
        return ANDROID_VERSION
    else:
        update.message.reply_text('Invalid Download Link. Submit A Proper Download Link!')
        return DOWNLOAD_LINK

def android_version(update: Update, context: CallbackContext) -> str:
    global NEW_ANDROID_VERSION
    NEW_ANDROID_VERSION = update.message.text
    user = update.message.from_user
    try:
        NEW_ANDROID_VERSION = int(NEW_ANDROID_VERSION)
    except ValueError:
        # Handle the exception
        update.message.reply_text('You havent entered an integer value, you had one task to do!')
        return ANDROID_VERSION
    return BUGS

def bugs(update: Update, context: CallbackContext) -> str:
    global NEW_BUGS
    NEW_BUGS = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send the flash steps needed in the form of a telegra.ph link.')
    return TELEGRAPH_FLASH_STEPS_LINK

def telegraph_flash_steps_link(update: Update, context: CallbackContext) -> str:
    global NEW_TELEGRAPH_FLASH_STEPS_LINK
    NEW_TELEGRAPH_FLASH_STEPS_LINK = update.message.text
    user = update.message.from_user
    if 'telegra.ph' in NEW_TELEGRAPH_FLASH_STEPS_LINK:
        update.message.reply_text('Send the Preferred gapps link ( press /skip only if your build ships with gapps).')
        return ARE_THERE_GAPPS
    else:
        update.message.reply_text('Telegra.ph Link is Invalid. Submit a proper link!')
        return TELEGRAPH_FLASH_STEPS_LINK

def are_there_gapps(update: Update, context: CallbackContext) -> str:
    global NEW_ARE_THERE_GAPPS, NEW_BUILD_TYPE
    NEW_ARE_THERE_GAPPS = update.message.text
    user = update.message.from_user
    if 'http' in NEW_ARE_THERE_GAPPS:
        update.message.reply_text('Build-Type=vanilla.')
        update.message.reply_text('Send the download Link of the recovery you\'d recommend your users to flash(Preferably anonfiles as files on anonfiles last a long time).')
        NEW_BUILD_TYPE='vanilla'
        return RECOVERY_DOWNLOAD_LINK
    else:
        update.message.reply_text('Gapps Link Is Invalid. Submit a proper link!.')
        return ARE_THERE_GAPPS

def recovery_download_link(update: Update, context: CallbackContext) -> int:
    global NEW_RECOVERY_DOWNLOAD_LINK
    NEW_RECOVERY_DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    if 'http' in NEW_RECOVERY_DOWNLOAD_LINK:
        update.message.reply_text('Send the firmware link if its needed ( /skip to skip).')
        return FIRMWARE_DOWNLOAD_LINK
    else:
        update.message.reply_text('Recovery Link Is Invalid. Submit a proper link!')
        return RECOVERY_DOWNLOAD_LINK

def firmware_download_link(update: Update, context: CallbackContext) -> str:
    global NEW_FIRMWARE_DOWNLOAD_LINK
    NEW_FIRMWARE_DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    if 'http' in NEW_FIRMWARE_DOWNLOAD_LINK:
        update.message.reply_text('Enter Changelog For Your Build.')
        return BUILD_CHANGELOG
    else:
        update.message.reply_text('Firmware Link Is Invalid. Provide a proper firmware link!')
        return FIRMWARE_DOWNLOAD_LINK

def build_changelog(update: Update, context: CallbackContext) -> str:
    global NEW_BUILD_CHANGELOG
    NEW_BUILD_CHANGELOG = update.message.text
    print(NEW_BUILD_CHANGELOG)
    user = update.message.from_user
    update.message.reply_text('Are there any Notes you\'d like to leave for users? (Enter /skip to skip notes).')
    return USER_NOTES

def user_notes(update: Update, context: CallbackContext) -> str:
    global NEW_USER_NOTES
    NEW_USER_NOTES = update.message.text
    user = update.message.from_user
    update.message.reply_text('Are The Above Values Correct? If Yes, Type "Y". Else Click /stop to start over again.')
    return ARE_VALUES_CORRECT

def are_values_correct(update: Update, context: CallbackContext) -> str:
    global NEW_ARE_VALUES_CORRECT
    NEW_ARE_VALUES_CORRECT = update.message.text.lower()
    user = update.message.from_user
    if 'y' in NEW_ARE_VALUES_CORRECT:
        update.message.reply_text('Processing Your Build.')
        NEW_ARE_VALUES_CORRECT='y'
        print('hello, this is a conformation test, implying that Your release has worked, this will show up in heroku logs')
        #process_build()
    elif 'n' in NEW_ARE_VALUES_CORRECT:
        update.message.reply_text('Aborted Processing of Build!.')
        NEW_ARE_VALUES_CORRECT='n'
    else:
        update.message.reply_text('Invalid Input Detected. Please enter \'y\' or \'n\'')
        return ARE_VALUES_CORRECT
    return ConversationHandler.END

def skip_bugs(update: Update, context: CallbackContext) -> str:
    global NEW_BUGS
    NEW_BUGS = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipping bugs. Now Send the flash steps needed in the form of a telegra.ph link.')
    return TELEGRAPH_FLASH_STEPS_LINK

def skip_are_there_gapps(update: Update, context: CallbackContext) -> str:
    global NEW_ARE_THERE_GAPPS, NEW_BUILD_TYPE
    NEW_ARE_THERE_GAPPS = 'skipped'
    NEW_BUILD_TYPE='gapps'
    user = update.message.from_user
    update.message.reply_text('Build-Type=gapps. Skipped GApps. Now Send the download Link of the recovery you\'d recommend your users to flash(Preferably anonfiles as files on anonfiles last a long time).')
    return RECOVERY_DOWNLOAD_LINK

def skip_firmware_download_link(update: Update, context: CallbackContext) -> str:
    global NEW_FIRMWARE_DOWNLOAD_LINK
    NEW_FIRMWARE_DOWNLOAD_LINK = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipped Firmware Download Link. Now Enter Changelog For Your Build.')
    return BUILD_CHANGELOG

def skip_user_notes(update: Update, context: CallbackContext) -> str:
    global NEW_USER_NOTES
    NEW_USER_NOTES = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipped Notes. Are The Above Values Correct? If Yes, Type "Y". Else Click /stop to start over again.')
    return ARE_VALUES_CORRECT

def stop(update: Update, context: CallbackContext) -> str:
    """Stops and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s stopped the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END

def main() -> str:
    """Run the bot."""
    
    # Create the Updater and pass it your bot's token.
    #updater = Updater(BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    #dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('release', release)],
        states={
            DEVICE_CODENAME: [MessageHandler(Filters.text & ~Filters.command, device_codename)],
            DEVICE_NAME: [MessageHandler(Filters.text & ~Filters.command, device_name)],
            OTA_STATUS: [MessageHandler(Filters.text & ~Filters.command, ota_status)],
            DOWNLOAD_LINK: [MessageHandler(Filters.text & ~Filters.command, download_link)],
            ANDROID_VERSION: [MessageHandler(Filters.text & ~Filters.command, android_version)],
            BUGS: [MessageHandler(Filters.text & ~Filters.command, bugs), CommandHandler('skip', skip_bugs)],
            TELEGRAPH_FLASH_STEPS_LINK: [MessageHandler(Filters.text & ~Filters.command, telegraph_flash_steps_link)],
            ARE_THERE_GAPPS: [MessageHandler(Filters.text & ~Filters.command, are_there_gapps), CommandHandler('skip', skip_are_there_gapps)],
            RECOVERY_DOWNLOAD_LINK: [MessageHandler(Filters.text & ~Filters.command, recovery_download_link)],
            FIRMWARE_DOWNLOAD_LINK: [MessageHandler(Filters.text & ~Filters.command, firmware_download_link), CommandHandler('skip', skip_firmware_download_link)],
            BUILD_CHANGELOG: [MessageHandler(Filters.text & ~Filters.command, build_changelog)],
            USER_NOTES: [MessageHandler(Filters.text & ~Filters.command, user_notes), CommandHandler('skip', skip_user_notes)],
            ARE_VALUES_CORRECT: [MessageHandler(Filters.text & ~Filters.command, are_values_correct)],
        },
        fallbacks=[CommandHandler('stop', stop)],
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

main()
