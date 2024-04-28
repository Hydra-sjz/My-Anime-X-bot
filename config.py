import os

from os import environ, mkdir, path, sys


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
GENIUS_API = os.getenv('GENIUS_API')
