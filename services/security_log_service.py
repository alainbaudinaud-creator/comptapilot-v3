from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = (
    "C:/Users/alain/mon-projet-agent/logs/security"
)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = (
    f"{LOG_DIR}/security.log"
)


logger = logging.getLogger("security_logger")

logger.setLevel(logging.INFO)


handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1000000,
    backupCount=5,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s"
)

handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


def log_security_event(event_type, message):

    logger.info(
        f"[{event_type}] {message}"
    )
