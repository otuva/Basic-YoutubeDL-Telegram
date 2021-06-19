# Basic-YoutubeDL-Telegram
Simple telegram bot for archiving things, ready to use right away.

---


### Usage:

0- Install docker

    sudo apt install docker-ce

<br>

1- Take bot token from Telegram's _BotFather_

<br>

2- Install dependencies

    docker pull capsulecode/singlefile
    docker tag capsulecode/singlefile singlefile
    pip3 install -r requirements.txt

<br>

3- Edit config.py (You might need to learn your chat id. _e.g. chat id echo bot_)

<br>

4- Run scripts respectively

    python3 init.py
    python3 main.py

<br>

5- Profit

- To download video or audio, use:
    
      /video <LINK>
      /song <LINK>
  
- To download other pages just send direct link to bot _e.g._:

      https://www.history.com/news/rats-didnt-spread-the-black-death-it-was-humans
---


Command | Description
------- | -----------
start   | Reply usage
video   | Download video
song    | Download song
