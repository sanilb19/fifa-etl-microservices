import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import kagglehub
from rich.console import Console
from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("extract")
console = Console()

def setup_directories():
    """Create necessary directories if they don't exist."""
    base_dir = Path("/app/data")
    dirs = {
        "raw": base_dir / "raw",
        "processed": base_dir / "processed",
        "archive": base_dir / "archive",
        "kagglehub": base_dir / "kagglehub"
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")
    
    return dirs

def download_from_kaggle(dirs):
    """Download dataset from Kaggle."""
    try:
        # Download the dataset
        logger.info("Downloading dataset from Kaggle...")
        kagglehub.model_download(
            "sanilbaweja/etl-with-dask",
            path=str(dirs["kagglehub"])
        )
        logger.info("Dataset downloaded successfully")
        
        # Move files to raw directory
        for file in dirs["kagglehub"].glob("*"):
            if file.is_file():
                target = dirs["raw"] / file.name
                file.rename(target)
                logger.info(f"Moved {file.name} to raw directory")
        
        return True
    except Exception as e:
        logger.error(f"Error downloading from Kaggle: {str(e)}")
        return False

def use_archive_data(dirs):
    """Use data from archive directory."""
    try:
        archive_dir = dirs["archive"]
        if not any(archive_dir.iterdir()):
            logger.error("Archive directory is empty")
            return False
            
        # Copy files from archive to raw
        for file in archive_dir.glob("*"):
            if file.is_file():
                target = dirs["raw"] / file.name
                file.rename(target)
                logger.info(f"Moved {file.name} from archive to raw directory")
        
        return True
    except Exception as e:
        logger.error(f"Error using archive data: {str(e)}")
        return False

def main():
    """Main extraction function."""
    try:
        # Setup directories
        dirs = setup_directories()
        
        # Get user input for data source
        while True:
            source = input("Choose data source (kaggle/archive): ").lower()
            if source in ["kaggle", "archive"]:
                break
            console.print("[red]Invalid choice. Please enter 'kaggle' or 'archive'[/red]")
        
        # Process based on user choice
        if source == "kaggle":
            success = download_from_kaggle(dirs)
        else:
            success = use_archive_data(dirs)
            
        if not success:
            logger.error("Data extraction failed")
            sys.exit(1)
            
        logger.info("Data extraction completed successfully")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 