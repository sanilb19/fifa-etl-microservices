import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Data paths
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARCHIVE_DATA_DIR = DATA_DIR / "archive"
KAGGLE_DATA_DIR = DATA_DIR / "kagglehub"

# Database settings
DB_CONNECTION_STRING = os.getenv(
    "DB_CONNECTION_STRING",
    "postgresql://postgres:postgres@localhost:5432/fifa"
)

# Dask settings
DASK_WORKERS = int(os.getenv("DASK_WORKERS", "4"))
DASK_MEMORY_LIMIT = os.getenv("DASK_MEMORY_LIMIT", "4GB")

# Kaggle settings
KAGGLE_DATASET = os.getenv("KAGGLE_DATASET", "stefanoleone992/fifa-21-complete-player-dataset")

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ARCHIVE_DATA_DIR, KAGGLE_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 