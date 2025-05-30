import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "data/archive"
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "postgresql://postgres:postgres@localhost:5432/fifa")
