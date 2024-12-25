import datetime
import geopandas as gpd
import numpy as np
import pandas as pd

import utils
from update_vars import OUTPUT_FOLDER, analysis_date, PROJECT_CRS, WGS84

if __name__ == "__main__":
    
    start = datetime.datetime.now()
    
    stop_times_with_geom = utils.get_stop_times_with_stop_geometry(analysis_date)
    t1 = datetime.datetime.now()
    print(f"stop_times + stop geom: {t1 - start}")
    
    stop_times_by_trip = utils.stop_time_by_trip(stop_times_with_geom)
    t2 = datetime.datetime.now()
    print(f"condense stop_times: {t2 - t1}")
    
    stop_times_direction_condensed = utils.find_direction_of_travel(stop_times_by_trip)
    t3 = datetime.datetime.now()
    print(f"add stop direction array: {t3 - t2}")
    
    stop_times_direction = utils.explode_arrays(stop_times_direction_condensed)
    t4 = datetime.datetime.now()
    print(f"explode: {t4 - t3}")
    
    gdf = pd.merge(
        stop_times_with_geom,
        stop_times_direction,
        on = ["feed_key", "trip_id", "stop_sequence"],
        how = "inner"
    ).to_crs(WGS84)
    
    gdf.to_parquet(f"{OUTPUT_FOLDER}stop_times_direction_{analysis_date}.parquet")    
    
    end = datetime.datetime.now()
    print(f"final df: {end - t4}")
    print(f"execution time: {end - start}")