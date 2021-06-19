import os
import config


def check_for_file(path):
    if os.path.isfile(path):
        pass
    else:
        os.mknod(path)


def check_for_dir(path):
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)


def main():
    print("checking for paths")
    check_for_dir(config.article_settings["path"])
    check_for_file(config.article_settings["archive-file"])