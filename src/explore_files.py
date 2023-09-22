# explore_files.py

import pandas as pd
import os
from settings import gtfs_dir

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 100)
# pd.set_option('display.max_rows', None)


def explore_files():
	agency_df = pd.read_csv(os.path.join(gtfs_dir, "agency.txt"))
	print("agency_df:")
	print(agency_df)

	calendar_dates_df = pd.read_csv(os.path.join(gtfs_dir, "calendar_dates.txt"))
	print("calendar_dates_df:")
	print(calendar_dates_df)

	calendar_df = pd.read_csv(os.path.join(gtfs_dir, "calendar.txt"))
	print("calendar_df:")
	print(calendar_df)

	routes_df = pd.read_csv(os.path.join(gtfs_dir, "routes.txt"))
	print("routes_df:")
	print(routes_df)

	shapes_df = pd.read_csv(os.path.join(gtfs_dir, "shapes.txt"))
	print("shapes_df:")
	print(shapes_df)

	stop_times_df = pd.read_csv(os.path.join(gtfs_dir, "stop_times.txt"))
	print("stop_times_df:")
	print(stop_times_df)

	trips_df = pd.read_csv(os.path.join(gtfs_dir, "trips.txt"))
	print("trips_df:")
	print(trips_df)

	stops_df = pd.read_csv(os.path.join(gtfs_dir, "stops.txt"))
	print("stops_df:")
	print(stops_df)
