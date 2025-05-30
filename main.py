from etl.extract import extract_from_csv
from etl.transform import clean_data
from etl.load import load_to_postgres
from utils.rich_utils import console

def main():
    console.log("Starting main execution")
    df = extract_from_csv()
    df_clean = clean_data(df)
    load_to_postgres(df_clean)
    console.log("Ended main execution")

if __name__ == "__main__":
    main()
