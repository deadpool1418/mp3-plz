"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from pytube import YouTube
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '2134398355:AAE9gSAG-G-qdu-fv-66KJuvQQvcuhDAtHI'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Send YouTube video url to get mp3.')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def sendSong(update, context):
        url = update.message.text;
        success = ''
        failure = ''
        if(update.message.chat.username == None):
            success = "Download your mp3 file... \n" + "Please set a username so I can call you with your username.\n" + "Have a great day " + "\U0001f600"
            failure = "Please check the url... \n" + "Please set a username so I can call you with your username.\n" + "Have a great day " + "\U0001f600"
        else:
            success = "Download your mp3 file... \n" + "Have a great day " + str(update.message.chat.username) + " " + "\U0001f600"
            failure = "Please check the url... \n" + "Have a great day " + str(update.message.chat.username) + " " + "\U0001f600"
        try:
            update.message.reply_text("Processing Your Request " + '\U0000231B')
            filename = downloadAudio(url)
            context.bot.send_audio(chat_id=update.message.chat_id, audio=open(filename, 'rb'))
            os.remove(filename)
            update.message.reply_text(success)
        except Exception as e:
            update.message.reply_text(failure)

def downloadAudio(url):
        video_url = url
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download()
        filenames = os.listdir('.')
        filename = ''
        for file in filenames:
            if file[-3:] == 'mp4':
                filename = file    
        return filename


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, sendSong))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://mp3-plz.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

