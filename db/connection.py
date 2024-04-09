from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_HOST = os.getenv('PG_HOST')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_PORT = os.getenv('PG_PORT')
PG_PASSWORD = os.getenv('PG_PASSWORD')

db = Connection(
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    database=os.getenv("PG_DATABASE"),
    host=os.getenv("PG_HOST"),
    port=int(os.getenv("PG_PORT"))
)
