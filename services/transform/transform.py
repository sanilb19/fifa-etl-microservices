import dask.dataframe as dd
import logging
from pathlib import Path
from rich.logging import RichHandler
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("transform")

def create_dask_dataframe(input_path: Path) -> dd.DataFrame:
    """Create Dask DataFrame from raw CSV"""
    return dd.read_csv(
        input_path,
        dtype={
            'contract_valid_until': 'float64',
            'league_rank': 'float64',
            'loaned_from': 'object',
            'release_clause_eur': 'float64',
            'team_jersey_number': 'float64'
        }
    )

def transform_data(df):
    """Transform the data using Dask."""
    try:
        logger.info("Starting data transformation...")
        
        # First, let's see what columns we have
        logger.info("Available columns:")
        for col in df.columns:
            logger.info(f"- {col}: {df[col].dtype}")
        
        # Handle missing values before categorical conversion
        logger.info("Handling missing values...")
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('unknown')
            elif df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(0)
        
        # Handle specific categorical columns we know about
        categorical_cols = ['position', 'nationality', 'preferred_foot', 'work_rate', 'body_type']
        for col in categorical_cols:
            if col in df.columns:
                logger.info(f"Converting {col} to categorical")
                try:
                    # Convert to categorical
                    df[col] = df[col].astype('category')
                    # Compute to ensure the conversion is complete
                    df[col] = df[col].compute()
                    logger.info(f"Successfully converted {col} to categorical")
                except Exception as e:
                    logger.error(f"Error converting {col}: {str(e)}")
                    raise
        
        # Create dummy variables for categorical columns
        for col in categorical_cols:
            if col in df.columns:
                logger.info(f"Creating dummy variables for {col}")
                try:
                    df = dd.get_dummies(df, columns=[col])
                    logger.info(f"Successfully created dummies for {col}")
                except Exception as e:
                    logger.error(f"Error creating dummies for {col}: {str(e)}")
                    raise
        
        logger.info("Transformation completed successfully")
        return df
        
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise

def main():
    """Main transformation function."""
    try:
        # Read data from raw directory
        raw_dir = Path("/app/data/raw")
        processed_dir = Path("/app/data/processed")
        
        # Ensure processed directory exists
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Read all CSV files in raw directory
        logger.info("Reading raw data...")
        df = create_dask_dataframe(raw_dir / "*.csv")
        
        # Transform data
        df_transformed = transform_data(df)
        
        # Save transformed data
        output_path = processed_dir / "transformed_data.parquet"
        logger.info(f"Saving transformed data to {output_path}")
        df_transformed.to_parquet(output_path)
        
        logger.info("Transformation completed successfully")
        
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 