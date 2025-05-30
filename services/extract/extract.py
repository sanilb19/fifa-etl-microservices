import kagglehub
import shutil
from pathlib import Path
import logging
import os
import json
from config.settings import RAW_DATA_DIR, KAGGLE_DATA_DIR, KAGGLE_DATASET, ARCHIVE_DATA_DIR

logger = logging.getLogger(__name__)

def setup_kaggle_auth():
    """Setup Kaggle authentication from environment variables if kaggle.json is not present"""
    kaggle_json = Path("/root/.kaggle/kaggle.json")
    logger.info(f"Checking for kaggle.json at {kaggle_json}")
    
    if not kaggle_json.exists():
        logger.info("kaggle.json not found, checking environment variables")
        username = os.getenv("KAGGLE_USERNAME", "").strip()
        key = os.getenv("KAGGLE_KEY", "").strip()
        
        if username and key:
            logger.info("Found Kaggle credentials in environment variables")
            # Create the kaggle.json with proper formatting
            credentials = {
                "username": username,
                "key": key
            }
            kaggle_json.parent.mkdir(parents=True, exist_ok=True)
            kaggle_json.write_text(json.dumps(credentials))
            kaggle_json.chmod(0o600)
            logger.info("Created kaggle.json from environment variables")
            # Verify the file was created correctly
            try:
                with open(kaggle_json, 'r') as f:
                    content = json.load(f)
                    logger.info("Verified kaggle.json format is correct")
            except Exception as e:
                logger.error(f"Error verifying kaggle.json: {str(e)}")
            return True
        else:
            logger.error("No Kaggle credentials found in environment variables")
    else:
        logger.info("Found existing kaggle.json")
        # Check if the file is readable and properly formatted
        try:
            with open(kaggle_json, 'r') as f:
                content = json.load(f)
                logger.info("kaggle.json is properly formatted")
        except json.JSONDecodeError as e:
            logger.error(f"kaggle.json is not valid JSON: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error reading kaggle.json: {str(e)}")
            return False
    
    return kaggle_json.exists()

def download_kaggle_dataset() -> bool:
    """Download FIFA dataset from Kaggle and return success status"""
    try:
        if not setup_kaggle_auth():
            logger.error("Kaggle authentication not set up. Please provide credentials.")
            return False

        # Download the dataset
        logger.info(f"Attempting to download dataset: {KAGGLE_DATASET}")
        try:
            # Try downloading with the dataset name
            logger.info(f"Downloading dataset: {KAGGLE_DATASET}")
            kagglehub.dataset_download(KAGGLE_DATASET, KAGGLE_DATA_DIR)
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            logger.error("Please verify your Kaggle credentials and dataset ID")
            return False
        
        # Find the downloaded CSV file
        csv_files = list(KAGGLE_DATA_DIR.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV files found in downloaded dataset")
        
        # Copy all CSV files to raw directory
        for source_path in csv_files:
            output_path = RAW_DATA_DIR / source_path.name
            shutil.copy2(source_path, output_path)
            logger.info(f"Dataset file copied to {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        return False

def use_archive_data() -> bool:
    """Use data from archive directory and return success status"""
    try:
        if not ARCHIVE_DATA_DIR.exists():
            logger.error(f"Archive directory {ARCHIVE_DATA_DIR} does not exist")
            return False
            
        # Check if archive is empty
        csv_files = list(ARCHIVE_DATA_DIR.glob("*.csv"))
        if not csv_files:
            logger.error("No CSV files found in archive directory")
            return False
            
        # Copy all CSV files to raw directory
        for source_path in csv_files:
            output_path = RAW_DATA_DIR / source_path.name
            shutil.copy2(source_path, output_path)
            logger.info(f"Archive file copied to {output_path}")
            
        return True
        
    except Exception as e:
        logger.error(f"Archive copy failed: {str(e)}")
        return False

def extract_data(source: str = "kaggle") -> bool:
    """Main extraction function that handles both Kaggle and archive sources"""
    try:
        # Ensure directories exist
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        KAGGLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
        ARCHIVE_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        if source.lower() == "kaggle":
            return download_kaggle_dataset()
        elif source.lower() == "archive":
            return use_archive_data()
        else:
            logger.error(f"Invalid source: {source}. Must be 'kaggle' or 'archive'")
            return False
            
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return False

def copy_local_file(source_path: Path, output_path: Path) -> None:
    """Copy local CSV file to output path"""
    try:
        shutil.copy2(source_path, output_path)
        logger.info(f"File copied to {output_path}")
    except Exception as e:
        logger.error(f"Copy failed: {str(e)}")
        raise 