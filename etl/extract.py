import dask.dataframe as dd
from etl.config import RAW_DATA_PATH
from rich.console import Console
import kagglehub

console = Console()

def extract_from_csv(file_name="players_21.csv"):
    file_path = RAW_DATA_PATH / file_name
    df = dd.read_csv(file_path, dtype={'contract_valid_until': 'float64',
       'league_rank': 'float64',
       'loaned_from': 'object',
       'release_clause_eur': 'float64',
       'team_jersey_number': 'float64'})
    
    console.print(df.head())
    return df

def extract_from_kaggle(url, path):
    kagglehub.dataset_download(url, path)
    file_path = RAW_DATA_PATH / path
    df = dd.read_csv(file_path, dtype={'contract_valid_until': 'float64',
       'league_rank': 'float64',
       'loaned_from': 'object',
       'release_clause_eur': 'float64',
       'team_jersey_number': 'float64'})
    console.print(df.head())
    return df