import os
from os import getenv
from os import environ, mkdir, path, sys


#PREFIX
CMDS = ["/","!",".","?","$","×",]


OWNER_ID = int(environ["OWNER_ID"])
SUDO_USERS = environ.get("SUDO_USERS", str(OWNER_ID)).split()

#MOMGO_DATABASE
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")

#API_TOOLS
CURRENCY_API = environ.get("CURRENCY_API")
GPT_API = os.environ.get("GPT_API")
DAXX_API = os.environ.get("DAXX_API")
DEEP_API = os.environ.get("DEEP_API")
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY','')
GENIUS_API = os.getenv('GEMINI_API')
GEMINI_API = os.getenv('GEMINI_API')
FORCE_SUB   = environ.get("FORCE_SUB", "XBOTS_X") 

#BORADCAST
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "784589736").split())
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001997285269"))
BOT_USERNAME = getenv("BOT_USERNAME", "gojosatorux_bot")
