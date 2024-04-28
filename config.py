import os

from os import environ, mkdir, path, sys


OWNER_ID = int(environ["OWNER_ID"])
SUDO_USERS = environ.get("SUDO_USERS", str(OWNER_ID)).split()

#MOMGO_DATABASE
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")
