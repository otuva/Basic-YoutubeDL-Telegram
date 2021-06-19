from bs4 import BeautifulSoup
import datetime
import requests
import hashlib
import config
import wget
import docker
import uuid
import os
import re

article_path = config.article_settings["path"]


def docker_down(link, file_name):
    print("\nlink: {}\nfile_name: {}\n".format(link, file_name))
    # os.system('docker run --rm singlefile "{0}" > {1}/{2}'.format(link,
    #                                                               config.article_settings["path"],
    #                                                               file_name))
    docker_client = docker.from_env()
    docker_image = docker_client.images.get("singlefile")

    docker_container = docker_client.containers.run(docker_image,
                                                    link,
                                                    auto_remove=True)

    file = open("{}/{}".format(article_path, file_name), "w")
    file.write(bytes.decode(docker_container))
    file.close()


def docker_handler(link):
    content_hash = hash_body_and_link(link)[0]
    link_hash = hash_body_and_link(link)[1]
    print("current content hash is {}".format(content_hash))
    if in_archive_already(content_hash, link_hash, config.article_settings["archive-file"]):
        print("already exist not downloading")
        return [1]

    else:
        file_name = file_name_formatter(link)

        try:
            print("file doesn't exist. docker started")
            print("downloading")

            docker_down(link, file_name)

            print("docker finished")

        except Exception as e:
            print("Exception: {}".format(e))
            return [2, e]

        else:
            print("successfully downloaded")
            append_in_archive(content_hash, link_hash, file_name, config.article_settings["archive-file"])
            return [0, file_name]


def pdf_file_namer(link):
    regexp_match = re.findall("(?<=\/)[\d\w\.]*(?=\.pdf)", link)
    new_file_name = ""
    if len(regexp_match) == 0:
        new_file_name = str(uuid.uuid4())
        new_file_name = new_file_name[:8]
    else:
        new_file_name = regexp_match[0]

    return "{}.pdf".format(new_file_name)



def pdf_handler(link):
    link_hash = hashlib.md5(bytes(link, encoding="utf8")).hexdigest()
    print("current pdf hash is {}".format(link_hash))
    if in_archive_already(link_hash, link_hash, config.article_settings["archive-file"]):
        print("already exist not downloading")
        return [1]

    else:
        file_name = pdf_file_namer(link)

        try:
            print("file doesn't exist. wget started")
            print("downloading")

            wget.download(link, "{}/{}".format(article_path, file_name))

            print("\nwget finished")

        except Exception as e:
            print("Exception: {}".format(e))
            return [2, e]

        else:
            print("successfully downloaded")
            append_in_archive(link_hash, link_hash, file_name, config.article_settings["archive-file"])
            return [0, file_name]


def append_in_archive(current_hash, link_hash, file_name, archive_file):
    file = open(archive_file, "a")
    file.write("{0} {1} {2}\n".format(current_hash, link_hash, file_name))
    file.close()


def in_archive_already(content_hash, link_hash, archive_file):
    file = open(archive_file, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        line_split = line.split()
        if line_split[0] == content_hash or line_split[1] == link_hash:
            return True

    return False


def hash_body_and_link(link):
    requested_link = requests.get(link, headers={"User-Agent": config.article_settings["User-Agent"]})
    # content_hash = hashlib.md5(requested_link.content).hexdigest()
    soup = BeautifulSoup(requested_link.text, features="lxml")
    response_body = soup.find("body").text
    content_hash = hashlib.md5(bytes(str(response_body), encoding="utf8")).hexdigest()
    link_hash = hashlib.md5(bytes(link, encoding="utf8")).hexdigest()
    # content_hash = hash(requested_link.content)
    return [content_hash, link_hash]

    # content_hash = hashlib.md5(link).hexdigest()
    # # content_hash = hash(requested_link.content)
    # return content_hash


def file_name_formatter(link) -> str:
    now = datetime.datetime.now()
    # date and time format: dd/mm/YYYY H:M:S
    date_format = "%d-%m-%Y_%H-%M-%S"
    current_time = now.strftime(date_format)

    if link.endswith("/"):
        link = link[:-1]

    # things_to_delete = ["https://", "www.", ".com", ".net", ".org", ".php"]
    things_to_delete = ["https://", "www.", ".php", ".html", ".txt"]

    for substr in things_to_delete:
        link = link.replace(substr, "")

    link = link.replace("/", "_")
    link = current_time + "_" + link + ".html"
    return link


def main(link):
    if link.endswith(".pdf"):
        return pdf_handler(link)
    else:
        return docker_handler(link)


if __name__ == '__main__':
    input_link = input("url: ")
    main(input_link)
