from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from youtube_dl.utils import DownloadError
import config
import re
import youtube_dl

users = config.users_allowed

def youtube_download(yt_link):
    try:
        links = [yt_link]
        youtube_opts = {"download_archive": "vids",
                        "format": "22",
                        "restrictfilenames": "true"}

        youtube = youtube_dl.YoutubeDL(youtube_opts)

        youtube.download(links)

    except DownloadError:
        return "INVALID LINK"

    except Exception as e:
        return "ERROR OCCURRED:\n\n\n{}".format(e)

    else:
        return "Downloading finished."


def start(update: Update, context: CallbackContext):
    update.message.reply_text("USAGE:\n\n/link <yt link>")


def link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # allowed users
    if user_id in users:
        value = update.message.text.split(" ")
        if len(value) != 2:
            update.message.reply_text("PROVIDE ONLY ONE LINK")

        elif re.search(r"&list=", value[1]):
            update.message.reply_text("ONLY VIDS OR PLAYLIST.\n")

        elif not value[1].startswith("https://"):
            update.message.reply_text("IT'S NOT A LINK'")

        else:
            update.message.reply_text("Downloading started.")
            update.message.reply_text(youtube_download(value[1]))
    else:
        update.message.reply_text("PERMISSION DENIED")


def main():
    bot_token = config.settings["bot_token"]
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    link_handler = CommandHandler('link', link)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(link_handler)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
