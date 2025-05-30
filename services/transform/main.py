import logging
from dask.distributed import Client
from pathlib import Path
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, DASK_WORKERS
from services.transform.transform import create_dask_dataframe, transform_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    client = Client(n_workers=DASK_WORKERS)
    
    try:
        # Read raw data
        input_path = RAW_DATA_DIR / 'players_21.csv'
        if not input_path.exists():
            raise FileNotFoundError(f"No raw data found at {input_path}")
        
        df = create_dask_dataframe(input_path)
        
        # Transform data
        df_transformed = transform_data(df)
        
        # Save transformed data
        output_path = PROCESSED_DATA_DIR / 'transformed.parquet'
        df_transformed.to_parquet(
            output_path,
            engine='pyarrow',
            compression='snappy'
        )
        
        logger.info("Transformation completed successfully")
        
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    main() 