import logging
import json
import random
import configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Benvenuto in CiaoItalia2015Bot! Ogni volta che lo invocherai, questo Bot ti invierà uno degli oltre 20.000 SMS inviati a "un famoso programma di Capodanno italiano"')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Per usare questo bot, invia il comando /new')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text('Per usare questo bot, invia il comando /new')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def new(update, context):
    """Send new SMS"""
    # Opening JSON file
    f = open('list.json', encoding='UTF-8')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Fetch SMS
    sms = data['sms']

    # Fetch random SMS
    msg = random.choice(sms)

    # Send data to user
    update.message.reply_text(msg)

    # Close file
    f.close()


def main():
    """Retrive token"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot = config["ciaoitalia2015"]["bot_token"]

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new", new))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
