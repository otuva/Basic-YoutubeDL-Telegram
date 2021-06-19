from src import commands

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import config


def main():
    bot_token = config.settings["bot_token"]
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', commands.start)
    video_handler = CommandHandler('video', commands.video)
    song_handler = CommandHandler('song', commands.song)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(video_handler)
    dispatcher.add_handler(song_handler)

    if config.article_settings["enabled"]:
        # non command text messages might contain article links.
        article_handler = MessageHandler(Filters.text, commands.link_listener)
        dispatcher.add_handler(article_handler)

    print("bot is started.")
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
