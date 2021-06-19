settings = {"bot_token": "<BOT_TOKEN>",
            "language": "tr",  # tr/en
            "yt_archive_file": "archive_files/vids"
            }

article_settings = {"enabled": True,
                    "path": "articles",
                    "User-Agent": "python-req",
                    "archive-file": "archive_files/pages"
                    }

youtube_audio = {"download_archive": settings["yt_archive_file"],
                 "format": "bestaudio",
                 "restrictfilenames": "true",
                 "outtmpl": "%(playlist)s/%(playlist_index)s-%(title)s-%(id)s.%(ext)s"
                 }

youtube_video = {"download_archive": settings["yt_archive_file"],
                 "format": "best",
                 "restrictfilenames": "true",
                 "outtmpl": "%(playlist)s/%(playlist_index)s-%(title)s-%(id)s.%(ext)s",
                 "cookiefile": "cookies.txt"
                 }

users_allowed = [USER2, USER1, USER0]
