
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Find the main SmartRoll project folder
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# Load local environment settings
load_dotenv(PROJECT_FOLDER / ".env")


def get_connection():
    """
    Connect to PostgreSQL.

    Online deployment:
        Uses DATABASE_URL if available.

    Local development:
        Uses DB_HOST, DB_PORT, DB_NAME,
        DB_USER and DB_PASSWORD.
    """

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
