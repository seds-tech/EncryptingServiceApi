import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGO_URI')
    }
    DEBUG = True

    def __init__(self):
        if not self.MONGODB_SETTINGS['host']:
            print("Warning: MONGO_URI is not set in the environment variables!")
        else:
            print(f"MONGO_URI: {self.MONGODB_SETTINGS['host']}")