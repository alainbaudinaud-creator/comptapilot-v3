import os

BASE_DIR = "C:/Users/alain/mon-projet-agent"
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")

SECRET_KEY = "change-moi-en-production"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "ifgsolutions16@gmail.com"
MAIL_PASSWORD = "suyv nlfcofuqpxxy"
MAIL_DEFAULT_SENDER = "ifgsolutions16@gmail.com"
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


