import kagglehub
import shutil
from pathlib import Path
import logging
from config.settings import RAW_DATA_DIR, KAGGLE_DATA_DIR, KAGGLE_DATASET

logger = logging.getLogger(__name__)

def download_kaggle_dataset() -> Path:
    """Download FIFA dataset from Kaggle and return the path to the downloaded file"""
    try:
        # Download the dataset
        logger.info(f"Downloading dataset from {KAGGLE_DATASET}")
        kagglehub.dataset_download(KAGGLE_DATASET, KAGGLE_DATA_DIR)
        
        # Find the downloaded CSV file
        csv_files = list(KAGGLE_DATA_DIR.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV files found in downloaded dataset")
        
        # Use the first CSV file found
        source_path = csv_files[0]
        output_path = RAW_DATA_DIR / source_path.name
        
        # Copy to raw data directory
        shutil.copy2(source_path, output_path)
        logger.info(f"Dataset downloaded and copied to {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise

def copy_local_file(source_path: Path, output_path: Path) -> None:
    """Copy local CSV file to output path"""
    try:
        shutil.copy2(source_path, output_path)
        logger.info(f"File copied to {output_path}")
    except Exception as e:
        logger.error(f"Copy failed: {str(e)}")
        raise 