from dotenv import load_dotenv
import os


load_dotenv()

DB_DATA = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "dnd-light"),
    "port": os.getenv("DB_PORT", "5432")
}