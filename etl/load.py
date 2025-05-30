from sqlalchemy import create_engine
import dask.dataframe as dd
from etl.config import DB_CONNECTION_STRING
from utils.rich_utils import console

def load_to_postgres(df, table_name="fifa_cleaned"):
    console.print("DB_CONNECTION_STRING", DB_CONNECTION_STRING)
    engine = create_engine(DB_CONNECTION_STRING)
    df.compute().to_sql(table_name, con=engine, if_exists='replace', index=False)
