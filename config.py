# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    API_KEY = os.getenv("API_KEY")
    DATABASE_URI = os.getenv("DATABASE_URI")
    DEBUG = os.getenv("DEBUG", "False") == "True"