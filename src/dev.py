# dev.py

from load_data import load_gtfs_data, afficher_df, save_data, load_data
from quality_of_service import explore_nested_dict, quality_of_service

# times_df, stops_df = load_gtfs_data()
# save_data(times_df, "times_df")
# save_data(stops_df, "stops_df")

# times_df = load_data("times_df")
# stops_df = load_data("stops_df")
# afficher_df(times_df, "times_df")
# afficher_df(stops_df, "stops_df")

# quality_data = quality_of_service(times_df, stops_df)
# save_quality_data(quality_data)
quality_data = load_data("quality_data")

explore_nested_dict(quality_data, level=1, length=True)

print("Done.")
