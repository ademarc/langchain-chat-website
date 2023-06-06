import os
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
import time

load_dotenv()

def get_openai_key():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return OPENAI_API_KEY

def get_db_creds():
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    return MONGODB_URI, MONGODB_DB_NAME

def setup_logging():

    LOG_DIR = 'logs/'
    os.makedirs(LOG_DIR, exist_ok=True)  # Ensure log directory exists

    # Define a custom formatter
    class CustomFormatter(logging.Formatter):
        converter = time.gmtime  # Convert time to UTC

        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            return time.strftime('%Y-%m-%dT%H:%M:%S', ct)

    # Initialize logger with level INFO
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up general log handler with rotation by day
    handler_info = TimedRotatingFileHandler(os.path.join(LOG_DIR, 'flask_combined.log'), when='midnight', backupCount=7)
    handler_info.setLevel(logging.INFO)
    handler_info.setFormatter(CustomFormatter('%(asctime)sZ info: %(message)s'))
    logger.addHandler(handler_info)

    # Set up error log handler with rotation by day
    handler_error = TimedRotatingFileHandler(os.path.join(LOG_DIR, 'flask_error.log'), when='midnight', backupCount=7)
    handler_error.setLevel(logging.ERROR)
    handler_error.setFormatter(CustomFormatter('%(asctime)sZ error: %(message)s'))
    logger.addHandler(handler_error)

    return logger
