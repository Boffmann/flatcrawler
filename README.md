# Python Flatcrawler

A telegram bot to find flats on Websites and simplifies to get in touch.
It works by parsing available flats from the website and sending those to you via telegram with all relevant data. Simply answer the bot to make it write a default message to the renter.

Inspired by [tschuehly's](https://github.com/tschuehly/flathunter) fork of the [flathunter](https://github.com/NodyHub/flathunter).
Most parts of this README copied from those but none of the code is.

## Setup

### Virtual Environment (Optional)
To keep you python environment and site-packages clean, it is recommended
to run the project in a virtual environment. Install `virtualenv`, create a venv and activate.

### Requirements
Install requirements from `requirements.txt` to run execute flathunter properly.
```
pip install -r requirements.txt
```

## Usage
```
usage: python flathunter.py --config CONFIG

Searches for flats on wg-gesucht.de and sends results to Telegram User

arguments:
  --config CONFIG, -c CONFIG
                        Config file to use. If not set, try to use
                        '~git-clone-dir/config.yaml'
```

Answer the bot with the following message to send your default message:
```
msg [id] [language]
  - [id] the advert's id (Send in message)
  - [language] It's possible to prepare the default message in multiple languages. [language] is the name of the specific file.
    - e.g. for msg [id] german the file "german.txt" is used
```



### Configuration

#### Bot registration
A new bot can registered with the telegram chat with the [BotFather](https://telegram.me/BotFather).

#### Chat-Ids
To get the chat id, the [REST-Api](https://core.telegram.org/bots/api) of telegram can be used to fetch the received messages of the Bot.
```
$ curl https://api.telegram.org/bot[BOT-TOKEN]/getUpdates
```

#### WG-Gesucht Credentials
In order to be able to send messages via WG-gesucht, one needs to log in. Therefore, enter your email and password from WG-gesucht to the config.
