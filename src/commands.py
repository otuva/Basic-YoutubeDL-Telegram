from src import yt_down
from src import bot_replies
from telegram import Update
from telegram.ext import CallbackContext
import config
import re

users = config.users_allowed
message = {}

if config.article_settings["enabled"]:
    from src import article_downloader

if config.settings["language"] == "tr":
    message = bot_replies.tr
elif config.settings["language"] == "en":
    message = bot_replies.en


def interpret_article_downloader(values):
    return_code = values[0]
    if return_code == 0:
        return message["article_success"].format(values[1])
    elif return_code == 1:
        return message["article_exists"]
    elif return_code == 2:
        return message["article_error"].format(values[1])


def link_listener(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in users:
        shared_link = ""
        link_found = False
        words = update.message.text.split()
        for word in words:
            if word.startswith("https://"):
                shared_link = word
                link_found = True
                break

        if link_found:
            print("Found link, getting information.")
            update.message.reply_text(message["article_getInfo"])
            return_values = article_downloader.main(shared_link)
            update.message.reply_text(interpret_article_downloader(return_values))

    else:
        print("user {} is not allowed".format(user_id))
        update.message.reply_text(message["what"])


def start(update: Update, context: CallbackContext):
    update.message.reply_text(message["help"])


def video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # allowed users
    if user_id in users:
        value = update.message.text.split(" ")
        if len(value) != 2:
            update.message.reply_text(message["yt_invalid0"])

        elif re.search(r"&list=", value[1]):
            update.message.reply_text(message["yt_invalid1"])

        elif not value[1].startswith("https://"):
            update.message.reply_text(message["yt_invalid2"])

        else:
            update.message.reply_text(message["yt_start"])
            update.message.reply_text(yt_down.video_download(value[1]))

    else:
        print("user {} is not allowed".format(user_id))
        update.message.reply_text(message["what"])


def song(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # allowed users
    if user_id in users:
        value = update.message.text.split(" ")
        if len(value) != 2:
            update.message.reply_text(message["yt_invalid0"])

        elif re.search(r"&list=", value[1]):
            update.message.reply_text(message["yt_invalid1"])

        elif not value[1].startswith("https://"):
            update.message.reply_text(message["yt_invalid2"])

        else:
            update.message.reply_text(message["yt_start"])
            update.message.reply_text(yt_down.audio_download(value[1]))
    else:
        print("user {} is not allowed".format(user_id))
        update.message.reply_text(message["what"])
