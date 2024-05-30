"""
Calculate stop arrivals per hour.
Compile weekday/weekend data and save
hourly stop arrivals for each operator by day_type.
"""
import pandas as pd

from dask import delayed, compute
from typing import Literal

DAY_TYPE_DICT = {
    "Monday": "weekday",
    "Tuesday": "weekday",
    "Wednesday": "weekday",
    "Thursday": "weekday",
    "Friday": "weekday",
    "Saturday": "weekend",
    "Sunday": "weekend"
}

def operator_stats(
    date_list: list
) -> pd.DataFrame:
    """
    Operator totals (look across all trips and stop_times).
    """
    trips_per_day = delayed(pd.concat)([
        pd.read_parquet(
            f"../data/stop_times_{d}.parquet",
            columns = ["name", "trip_id"]
        ).drop_duplicates() for d in date_list
    ], axis=0)

    trips_per_week = (trips_per_day
                      .groupby("name")
                      .agg({"trip_id": "count"})
                      .reset_index()
                      .rename(columns = {"trip_id": "n_trips"})
                     )
        
    trips_per_week = compute(trips_per_week)[0]
    
    return trips_per_week
    

def stop_arrivals_per_hour(
    df: pd.DataFrame,
    group_cols: list,
    aggfunc: Literal["count", "sum"]
) -> pd.DataFrame:
    """
    Count number of scheduled stop arrivals
    over a grouping of columns.
    If we've already used this to count, then we
    want to take the sum downstream.
    """
    df2 = (df
           .groupby(group_cols, observed=True, group_keys=False)
           .agg({"stop_sequence": aggfunc})
           .reset_index()
          )
    
    return df2


def expand_rows_fill_with_zeros(
    df: pd.DataFrame,
    group_cols: list
) -> pd.DataFrame:
    """
    Use group_cols to uniquely identify a row that we want to expand 
    and fill in rows that don't have service with zeros. 
    We want every hour to be present, even if there was no service.
    """    
    # Set the iterables to be exact order as group_cols        
    iterables = [
        *[df[c].unique() for c in group_cols]
    ]
    
    multi_ix = pd.MultiIndex.from_product(
        iterables, 
        names = group_cols
    )
    
    df2 = df.set_index(group_cols)
    df2 = df2[~df2.index.duplicated(keep="first")]
    
    df_expanded = (df2.reindex(multi_ix)
                   .reset_index()
                  )
    
    # Fill with zeroes
    df_expanded = df_expanded.assign(
        stop_sequence = df_expanded.stop_sequence.fillna(0),
    ).astype({
        "arrival_hour": "int8",
        "stop_sequence": "int"
    })
    
    return df_expanded


def stop_arrivals_single_day(date: str):
    
    df = pd.read_parquet(
        f"../data/stop_times_{date}.parquet"
    ).pipe(
        stop_arrivals_per_hour, 
        group_cols = ["name", "arrival_hour"],
        aggfunc="count"
    )
    
    df2 = expand_rows_fill_with_zeros(
        df, group_cols = ["name", "arrival_hour"],
    )
    
    return df2
  
        
def transform_arrivals_for_polars_df(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Taking a look at now great-tables nanoplots work,
    we need a column that is a list and holds 
    the values we want to plot.
    
    Operator1   [weekday_arrival_list]  [weekend_arrival_list]
    Operator2   [weekday_arrival_list]  [weekend_arrival_list]
    """
    # Transform long df into condensed version of arrivals (hold as list)
    group_cols = ["name", "day_type"]
    
    df2 = (df.sort_values(group_cols + ["arrival_hour"])
     .groupby(group_cols)
     .agg({
         "n_arrivals": lambda x: list(x)})
     .reset_index()
    )

    # Transform from long to wide, so weekday and weekend arrivals
    # are separate columns
    df3 = df2.pivot(
        index="name", 
        columns = "day_type", 
        values="n_arrivals"
    ).reset_index().rename(
        columns = {
            "weekday": "weekday_arrivals",
            "weekend": "weekend_arrivals"
        }
    ).set_index("name")
    
    df4 = pd.merge(
        df[["name", "n_trips"]].drop_duplicates().set_index("name"),
        df3,
        on = "name",
        how = "inner"
    ).reset_index()
    
    return df4


if __name__ == "__main__":
    
    from variables import date_list
    
    # For the list of 7 dates, read in the df and aggregate
    # Add a column for weekday/weekend called day_type
    dfs = [
        stop_arrivals_single_day(d)
        .assign(
            day_name = pd.to_datetime(d).day_name()
        ) for d in date_list
    ]
    
    # Concatenate list of aggregated hourly arrivals
    # and aggregate again. Instead of a row for Monday, Tuesday, we 
    # want only a row for weekday and weekend
    df = pd.concat(dfs, axis=0, ignore_index=True)
    
    arrivals_per_hour = df.assign(
        # Instead of Mon, Tues, Wed, we want weekday or weekend
        day_type = df.day_name.map(DAY_TYPE_DICT)
    ).pipe(
        stop_arrivals_per_hour,    
        group_cols = ["name", "arrival_hour", "day_type"],
        aggfunc="sum"
    ).rename(columns = {"stop_sequence": "n_arrivals"})
    
    operator_trips = operator_stats(date_list)
    
    arrivals_per_hour2 = pd.merge(
        arrivals_per_hour,
        operator_trips,
        on = "name",
        how = "inner"
    )
    
    arrivals_per_hour2 = arrivals_per_hour2.assign(
        # Clean up operator name
        name = arrivals_per_hour2.name.str.replace('Schedule', '').str.strip(),
    )
    
    arrivals_per_hour2.to_parquet("../data/arrivals_per_hour.parquet")
    
    
    arrivals_per_hour = pd.read_parquet("../data/arrivals_per_hour.parquet")
    
    arrivals_transformed = transform_arrivals_for_polars_df(arrivals_per_hour)
    arrivals_transformed.to_parquet("../data/arrivals_polars.parquet")