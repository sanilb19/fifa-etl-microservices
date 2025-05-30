import os
import sys
import logging
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from services.extract.extract import extract_data

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("extract")
console = Console()

def main():
    """Main extraction function."""
    try:
        # Get data source from environment variable
        source = os.getenv("DATA_SOURCE", "").lower()
        
        # Validate source
        if not source:
            logger.error("DATA_SOURCE environment variable not set")
            logger.info("Please set DATA_SOURCE to either 'kaggle' or 'archive'")
            logger.info("Example: DATA_SOURCE=kaggle docker-compose up --build")
            sys.exit(1)
            
        if source not in ["kaggle", "archive"]:
            logger.error(f"Invalid DATA_SOURCE value: {source}")
            logger.info("DATA_SOURCE must be either 'kaggle' or 'archive'")
            sys.exit(1)
        
        # Process based on source choice
        logger.info(f"Using data source: {source}")
        success = extract_data(source)
            
        if not success:
            logger.error("Data extraction failed")
            sys.exit(1)
            
        logger.info("Data extraction completed successfully")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 