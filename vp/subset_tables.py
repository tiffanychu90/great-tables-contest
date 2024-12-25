import geopandas as gpd
import pandas as pd

from update_vars import analysis_date, INPUT_FOLDER, OUTPUT_FOLDER

def unique_rt_trips(analysis_date: str) -> pd.DataFrame:
    """
    Get df of unique RT trips to produce sample data.
    """
    # Get only operators have RT
    rt_operators = pd.read_parquet(
        f"{INPUT_FOLDER}vp_{analysis_date}.parquet",
        columns = ["trip_instance_key"]
    ).drop_duplicates()
    
    schedule_trips = pd.read_parquet(
        f"{INPUT_FOLDER}trips_{analysis_date}.parquet",
        columns = ["name", "gtfs_dataset_key", "feed_key",
                   "trip_id", "shape_id", "trip_instance_key"],
        filters = [[
            ("trip_instance_key", "in", rt_operators.trip_instance_key.unique().tolist())
        ]]
    ).rename(columns = {"gtfs_dataset_key": "schedule_gtfs_dataset_key"}).drop_duplicates()
    
    return schedule_trips
 

def sample_by_trips_and_export(
    table_name: str, 
    sample_table: pd.DataFrame
): 
    subset_feeds = sample_table.feed_key.unique().tolist()
    subset_trips = rt_trips.trip_id.unique().tolist()
    subset_operators = rt_trips.schedule_gtfs_dataset_key.unique().tolist()
    subset_shapes = rt_trips.shape_id.unique().tolist()
    
    crosswalk = pd.read_parquet(
        f"{INPUT_FOLDER}trips_{analysis_date}.parquet",
        filters = [[("feed_key", "in", subset_feeds)]],
        columns = ["feed_key", "gtfs_dataset_key"]
    ).drop_duplicates().rename(columns = {"gtfs_dataset_key": "schedule_gtfs_dataset_key"})
    
    if table_name in ["trips", "stop_times"]:
        df = pd.read_parquet(
            f"{INPUT_FOLDER}{table_name}_{analysis_date}.parquet",
            filters = [[
                ("feed_key", "in", subset_feeds),
                ("trip_id", "in", subset_trips),
            ]]
        ).merge(
            crosswalk,
            on = "feed_key",
            how = "inner"
        ).drop(columns = "feed_key")
    
    elif table_name == "shapes":
        df = gpd.read_parquet(
            f"{INPUT_FOLDER}{table_name}_{analysis_date}.parquet",
            filters = [[
                ("feed_key", "in", subset_feeds),
                ("shape_id", "in", subset_shapes)
            ]]
        ).merge(
            crosswalk,
            on = "feed_key",
            how = "inner"
        ).drop(columns = "feed_key")
        
    elif table_name in ["stops", "stop_times_direction"]:
        df = gpd.read_parquet(
            f"{INPUT_FOLDER}{table_name}_{analysis_date}.parquet",
            filters = [[("feed_key", "in", subset_feeds)]]
        ).merge(
            crosswalk,
            on = "feed_key",
            how = "inner"
        ).drop(columns = "feed_key")
        
        
    elif table_name == "vp":
        df = gpd.read_parquet(
            f"{INPUT_FOLDER}{table_name}_{analysis_date}.parquet",
            filters = [[
                ("schedule_gtfs_dataset_key", "in", subset_operators),
                ("trip_id", "in", subset_trips)
            ]]
        )
    
    df.to_parquet(f"{OUTPUT_FOLDER}{table_name}_{analysis_date}.parquet")
    print(f"exported {table_name}")
    
    return 

if __name__ == "__main__":
    subset_operators = [
        "LA DOT Schedule",
    ]
    
    rt_trips = unique_rt_trips(analysis_date)
    rt_trips = rt_trips[rt_trips.name.isin(subset_operators)]
    
    files = [
        "trips", "shapes", "stops", "stop_times",
        "vp", "stop_times_direction"
    ]
    
    for f in files:
        sample_by_trips_and_export(f, rt_trips)

    

    

        
        
    