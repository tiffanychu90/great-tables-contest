import pandas as pd

GCS_FILE_PATH = (
    "gs://calitp-analytics-data/data-analyses/"
    "rt_delay/compiled_cached_views/"
)

start_date = "2024-04-15"
end_date = "2024-04-21"

date_range = pd.date_range(start=start_date, end=end_date)
date_list = [pd.to_datetime(i).date().isoformat()
             for i in date_range]