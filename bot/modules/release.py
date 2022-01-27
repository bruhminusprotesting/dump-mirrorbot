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

GENDER, PHOTO, LOCATION, BIO = range(4)

def release(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    #if user.id in AUTHORIZED_CHATS:
    #    print(user.id)
    #else:
    #    update.message.reply_text(
    #            "This is a temp restricted command."
    #            " You do not have permissions to run this.")
    #    stop()
    if not user.id in AUTHORIZED_CHATS or not user.id in SUDO_USERS:
            update.message.reply_text(
                "This is a temp restricted command."
                " You do not have permissions to run this.")
            stop()
        
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        "Enter Your Device Codename."
        "Use /stop to exit."
    )
    return DEVICE_CODENAME
    #return DEVICE_NAME

def device_codename(update: Update, context: CallbackContext) -> int:
    """Stores the device_codename and asks for device_name."""
    global DEVICE_CODENAME
    DEVICE_CODENAME = update.message.text
    user = update.message.from_user
    update.message.reply_text(
        'Send Your Device Name(example: Realme C1):',
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEVICE_NAME

def device_name(update: Update, context: CallbackContext) -> int:
    """Stores the device_name and asks for OTA Status."""
    global DEVICE_NAME
    DEVICE_NAME = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send Your Device Name(example: Realme C1):')
    return OTA_STATUS

def ota_status(update: Update, context: CallbackContext) -> int:
    """Stores Device Name And Asks For OTA Status."""
    global OTA_STATUS
    OTA_STATUS = update.message.text
    user = update.message.from_user
    update.message.reply_text('Do You Want To Send an OTA Update To Users For This Build? (y/n).')
    return DOWNLOAD_LINK

def download_link(update: Update, context: CallbackContext) -> int:
    """Stores OTA Info and asks for download link."""
    global DOWNLOAD_LINK
    DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    update.message.reply_text('What\'s the android version?(integer values only).')
    return ANDROID_VERSION

def android_version(update: Update, context: CallbackContext) -> int:
    global ANDROID_VERSION
    ANDROID_VERSION = update.message.text
    user = update.message.from_user
    update.message.reply_text('Are there any bugs you\'d like to inform your users about?( /skip to skip).')
    return BUGS

def bugs(update: Update, context: CallbackContext) -> int:
    global BUGS
    BUGS = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send the flash steps needed in the form of a telegra.ph link.')
    return TELEGRAPH_FLASH_STEPS_LINK

def telegraph_flash_steps_link(update: Update, context: CallbackContext) -> int:
    global TELEGRAPH_FLASH_STEPS_LINK
    TELEGRAPH_FLASH_STEPS_LINK = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send the Preferred gapps link ( press /skip only if your build ships with gapps).')
    return ARE_THERE_GAPPS

def are_there_gapps(update: Update, context: CallbackContext) -> int:
    global ARE_THERE_GAPPS
    ARE_THERE_GAPPS = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send the download Link of the recovery you\'d recommend your users to flash(Preferably anonfiles as files on anonfiles last a long time).')
    return RECOVERY_DOWNLOAD_LINK

def recovery_download_link(update: Update, context: CallbackContext) -> int:
    global RECOVERY_DOWNLOAD_LINK
    RECOVERY_DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    update.message.reply_text('Send the firmware link if its needed ( /skip to skip).')
    return FIRMWARE_DOWNLOAD_LINK

def firmware_download_link(update: Update, context: CallbackContext) -> int:
    global FIRMWARE_DOWNLOAD_LINK
    FIRMWARE_DOWNLOAD_LINK = update.message.text
    user = update.message.from_user
    update.message.reply_text('Enter Changelog For Your Build.')
    return BUILD_CHANGELOG

def build_changelog(update: Update, context: CallbackContext) -> int:
    global BUILD_CHANGELOG
    BUILD_CHANGELOG = update.message.text
    user = update.message.from_user
    update.message.reply_text('Are there any Notes you\'d like to leave for users? (Enter /skip to skip notes).')
    return USER_NOTES

def user_notes(update: Update, context: CallbackContext) -> int:
    global USER_NOTES
    USER_NOTES = update.message.text
    user = update.message.from_user
    update.message.reply_text('Are The Above Values Correct? If Yes, Type "Y". Else Click /stop to start over again.')
    return ARE_VALUES_CORRECT

def are_values_correct(update: Update, context: CallbackContext) -> int:
    global ARE_VALUES_CORRECT
    ARE_VALUES_CORRECT = update.message.text
    user = update.message.from_user
    update.message.reply_text('Processing Your Build.')
    print('hello, this is a conformation test')
    return ConversationHandler.END
    #process_build()

def skip_bugs(update: Update, context: CallbackContext) -> int:
    global BUGS
    BUGS = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipping bugs. Now Send the flash steps needed in the form of a telegra.ph link.')
    return TELEGRAPH_FLASH_STEPS_LINK

def skip_are_there_gapps(update: Update, context: CallbackContext) -> int:
    global ARE_THERE_GAPPS
    ARE_THERE_GAPPS = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipped GApps. Now Send the download Link of the recovery you\'d recommend your users to flash(Preferably anonfiles as files on anonfiles last a long time).')
    return RECOVERY_DOWNLOAD_LINK

def skip_firmware_download_link(update: Update, context: CallbackContext) -> int:
    global FIRMWARE_DOWNLOAD_LINK
    FIRMWARE_DOWNLOAD_LINK = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Skipped Firmware Download Link. Now Enter Changelog For Your Build.')
    return BUILD_CHANGELOG

def skip_user_notes(update: Update, context: CallbackContext) -> int:
    global USER_NOTES
    USER_NOTES = 'skipped'
    user = update.message.from_user
    update.message.reply_text('Are The Above Values Correct? If Yes, Type "Y". Else Click /stop to start over again.')
    return ARE_VALUES_CORRECT

def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    print("Hello")
    print(DEVICE_CODENAME)
    print("Should work")
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def stop(update: Update, context: CallbackContext) -> int:
    """Stops and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s stopped the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    
    # Create the Updater and pass it your bot's token.
    #updater = Updater(BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    #dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('release', release)],
        states={
            DEVICE_CODENAME: [MessageHandler(Filters.text, device_codename)],
            DEVICE_NAME: [MessageHandler(Filters.text, device_name)],
            OTA_STATUS: [MessageHandler(Filters.text, ota_status)],
            DOWNLOAD_LINK: [MessageHandler(Filters.text, download_link)],
            ANDROID_VERSION: [MessageHandler(Filters.text, android_version)],
            BUGS: [MessageHandler(Filters.text, bugs), CommandHandler('skip', skip_bugs)],
            TELEGRAPH_FLASH_STEPS_LINK: [MessageHandler(Filters.text, telegraph_flash_steps_link)],
            ARE_THERE_GAPPS: [MessageHandler(Filters.text, are_there_gapps), CommandHandler('skip', skip_are_there_gapps)],
            RECOVERY_DOWNLOAD_LINK: [MessageHandler(Filters.text, recovery_download_link)],
            FIRMWARE_DOWNLOAD_LINK: [MessageHandler(Filters.text, firmware_download_link), CommandHandler('skip', skip_firmware_download_link)],
            BUILD_CHANGELOG: [MessageHandler(Filters.text, build_changelog)],
            USER_NOTES: [MessageHandler(Filters.text, user_notes), CommandHandler('skip', skip_user_notes)],
            ARE_VALUES_CORRECT: [MessageHandler(Filters.text, DEVICE_NAME)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)

main()
