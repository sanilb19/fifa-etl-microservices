import logging
from pathlib import Path
import pandas as pd
import dask.dataframe as dd
from sqlalchemy import create_engine, text
from rich.logging import RichHandler
from typing import Optional, Union
from config.settings import DB_CONNECTION_STRING

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("load")

class DataLoader:
    def __init__(self, db_url):
        """Initialize the data loader with database connection."""
        # Replace localhost with postgres service name
        db_url = db_url.replace("localhost", "postgres")
        logger.info(f"Connecting to database at {db_url}")
        self.engine = create_engine(db_url)
        self.table_name = "fifa_players"

    def _create_table_if_not_exists(self, df: Union[pd.DataFrame, dd.DataFrame]):
        """Create the table if it doesn't exist."""
        try:
            # Get a sample of the data to determine schema
            if isinstance(df, dd.DataFrame):
                logger.info("Computing sample from Dask DataFrame...")
                # Get the first partition and compute it
                sample_df = df.get_partition(0).compute()
            else:
                logger.info("Getting sample from pandas DataFrame...")
                sample_df = df.head(1)

            # Create table with appropriate schema
            logger.info(f"Creating table {self.table_name} with schema...")
            sample_df.to_sql(
                self.table_name,
                self.engine,
                if_exists='replace',
                index=False
            )
            logger.info(f"Created table {self.table_name}")
        except Exception as e:
            logger.error(f"Error creating table: {str(e)}")
            raise

    def load_data(self, df: Union[pd.DataFrame, dd.DataFrame]):
        """Load data into the database."""
        try:
            logger.info("Starting data load...")
            
            # Verify DataFrame type
            if not isinstance(df, (pd.DataFrame, dd.DataFrame)):
                raise TypeError(f"Expected pandas or dask DataFrame, got {type(df)}")
            
            # Create table if it doesn't exist
            self._create_table_if_not_exists(df)
            
            # Load data in chunks
            if isinstance(df, dd.DataFrame):
                # For Dask DataFrame, compute and load in chunks
                logger.info("Loading Dask DataFrame in chunks...")
                n_partitions = df.npartitions
                logger.info(f"Total partitions to process: {n_partitions}")
                
                # Convert to pandas DataFrame in chunks
                for i in range(n_partitions):
                    logger.info(f"Loading partition {i+1}/{n_partitions}...")
                    partition = df.get_partition(i).compute()
                    if not isinstance(partition, pd.DataFrame):
                        partition = pd.DataFrame(partition)
                    partition.to_sql(
                        self.table_name,
                        self.engine,
                        if_exists='append',
                        index=False
                    )
            else:
                # For pandas DataFrame, load directly
                logger.info("Loading pandas DataFrame...")
                df.to_sql(
                    self.table_name,
                    self.engine,
                    if_exists='append',
                    index=False
                )
            
            logger.info("Data load completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            raise

def main():
    """Main loading function."""
    try:
        # Read transformed data
        processed_dir = Path("/app/data/processed")
        input_path = processed_dir / "transformed_data.parquet"
        
        logger.info(f"Reading transformed data from {input_path}")
        df = dd.read_parquet(input_path)
        
        # Initialize loader with database URL
        db_url = "postgresql://postgres:postgres@postgres:5432/fifa_db"
        loader = DataLoader(db_url)
        
        # Load data
        loader.load_data(df)
        
        logger.info("Loading completed successfully")
        
    except Exception as e:
        logger.error(f"Loading failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 