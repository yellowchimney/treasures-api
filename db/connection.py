"""This module handles db connection with .env variables"""

from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv()


def connect_to_db():
    return Connection(
        user=os.getenv("PG_USER"),
        database=os.getenv("PG_DATABASE"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
    )
