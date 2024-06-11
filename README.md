# great-tables-contest
Good to great tables

## Transit Service Patterns in California

Have you ever been curious about transit service patterns in California? What would hourly service patterns tell us about the types of riders the operator is oriented to serve?

Service geared towards commuters have pronounced camel peaks during the AM and PM peak commuting hours. Service geared towards travelers would provide mostly consistent service throughout the day. After all, travelers passing through the airport expect to catch a shuttle, no matter the time-of-day.

We can use GTFS scheduled stop times to count the number of arrivals for each hour of the day and look at how weekday and weekend service differ by operators. Within each Caltrans District, operators are sorted according to the number of weekly trip volume. 

A `great_tables` nanoplot is a great way to convey, at a glance, the operator’s hourly service profile while situating the operator’s service in a regional context.

## Everything You Need
* [Raw and processed datasets](https://github.com/tiffanychu90/great-tables-contest/blob/main/data/) backing the table
* Data cleaning [script](https://github.com/tiffanychu90/great-tables-contest/blob/main/scripts/aggregate.py)
* What is the [General Transit Feed Specification (GTFS)](https://gtfs.org) and what is in the [stop_times](https://gtfs.org/schedule/reference/#stop_timestxt) table?
* What is the Caltrans [Division of Data and Digital Services](https://www.calitp.org/) about and what are our other [analysis products](https://analysis.calitp.org)?
* Reach out to [Cal-ITP](mailto:hello@calitp.org) or [Tiffany](mailto:tiffany.ku@dot.ca.gov)

## Reproducing the Table
* If you have Docker installed, run `docker compose build` (the first time) and `docker compose up` to start up the container.
   * This is the same environment backing Cal-ITP's JupyterHub with no changes (by design!)
* To install several other packages used in this repository, `cd great-tables-contest/` and run `make install_env`.
* To take the raw data and transform it into the processed data frame for the table, run `make process_data`.