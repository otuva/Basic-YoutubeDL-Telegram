from src import bot_replies
import youtube_dl
import config

message = {}

if config.settings["language"] == "tr":
    message = bot_replies.tr
elif config.settings["language"] == "en":
    message = bot_replies.en


def audio_download(link) -> str:
    try:
        links = [link]
        youtube_opts = config.youtube_audio

        youtube = youtube_dl.YoutubeDL(youtube_opts)

        youtube.download(links)

    except Exception as e:
        return message["yt_error"].format(e)

    else:
        return message["yt_success"]


def video_download(yt_link) -> str:
    try:
        links = [yt_link]
        youtube_opts = config.youtube_video

        youtube = youtube_dl.YoutubeDL(youtube_opts)

        youtube.download(links)

    except Exception as e:
        return message["yt_error"].format(e)

    else:
        return message["yt_success"]
