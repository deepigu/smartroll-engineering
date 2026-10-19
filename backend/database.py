
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Find the main SmartRoll folder
project_folder = Path(__file__).resolve().parent.parent

# Load database settings from .env
load_dotenv(project_folder / ".env")


# Function to connect to PostgreSQL
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
