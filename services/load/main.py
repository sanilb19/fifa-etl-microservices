import logging
from dask.distributed import Client
from pathlib import Path
from config.settings import PROCESSED_DATA_DIR, DASK_WORKERS, DB_CONNECTION_STRING
from services.load.load import DataLoader
import dask.dataframe as dd
import pandas as pd
from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

def main():
    # Initialize Dask client
    logger.info(f"Initializing Dask client with {DASK_WORKERS} workers...")
    client = Client(n_workers=DASK_WORKERS)
    
    try:
        # Read transformed data
        input_path = PROCESSED_DATA_DIR / 'transformed.parquet'
        if not input_path.exists():
            raise FileNotFoundError(f"No processed data found at {input_path}")
        
        logger.info(f"Reading transformed data from {input_path}")
        
        # Create Dask DataFrame directly from parquet
        logger.info("Creating Dask DataFrame from parquet...")
        df = dd.read_parquet(input_path)
        
        # Verify it's a Dask DataFrame
        if not isinstance(df, dd.DataFrame):
            raise TypeError(f"Expected Dask DataFrame, got {type(df)}")
            
        logger.info(f"Created Dask DataFrame with {len(df.columns)} columns and {df.npartitions} partitions")
        
        # Initialize loader with database URL
        logger.info("Initializing database connection...")
        db_url = "postgresql://postgres:postgres@postgres:5432/fifa_db"
        loader = DataLoader(db_url)
        
        # Load data
        logger.info("Starting data load...")
        loader.load_data(df)
        logger.info("Data load completed successfully")
        
    except Exception as e:
        logger.error(f"Loading failed: {str(e)}")
        raise
    finally:
        logger.info("Closing Dask client...")
        client.close()

if __name__ == "__main__":
    main() 