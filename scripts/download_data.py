"""
Grab a week's worth of GTFS stop_times data
from our Google Cloud Storage bucket.
"""
import pandas as pd 

from variables import GCS_FILE_PATH

def create_stop_times_data(
    date: str
) -> pd.DataFrame:
    """
    Grab the stop_times table and add columns
    to find the operator name.
    """
    stop_times = pd.read_parquet(
        f"{GCS_FILE_PATH}st_{date}.parquet",
    )
    
    operator_info = pd.read_parquet(
        f"{GCS_FILE_PATH}trips_{date}.parquet",
        columns = ["feed_key", "name"]
    ).drop_duplicates()
    
    df = pd.merge(
        stop_times,
        operator_info,
        on = "feed_key",
        how = "inner"
    )
    
    return df
    

if __name__ == "__main__":
    
    from variables import date_list
    
    for date in date_list:
        df = create_stop_times_data(date)
        df.to_parquet(f"../data/stop_times_{date}.parquet")
