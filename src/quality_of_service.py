# quality_of_service.py

import pandas as pd
from tqdm import tqdm


def quality_of_service(times_df, stops_df):
	# Create a list of time strings in HH:MM:SS format
	time_strings = [f"{hour:02d}:{minute:02d}:00" for hour in range(24) for minute in range(0, 60, 15)]

	# Create a DataFrame with the time intervals
	time_intervals = pd.DataFrame({'time_interval': time_strings})

	# Convert 'time_interval' column to Timestamp objects
	time_intervals['time_interval'] = pd.to_datetime(time_intervals['time_interval'], format='%H:%M:%S').dt.time

	# Get the total number of time intervals
	total_intervals = len(time_intervals)

	# Convert 'departure_time' column to Timestamp objects
	times_df['departure_time'] = pd.to_datetime(times_df['departure_time'], format='%H:%M:%S').dt.time

	# Pre-process stops_df into a dictionary for efficient lookups
	stops_dict = {}
	for index, row in stops_df.iterrows():
		stop_id = row['stop_id']
		stop_lat = row['stop_lat']
		stop_lon = row['stop_lon']
		stops_dict[stop_id] = {'stop_lat': stop_lat, 'stop_lon': stop_lon}

	# Create an empty dictionary to hold the structured data
	quality_data = {}

	# Use tqdm to create a progress bar
	with tqdm(total=total_intervals, desc="Processing") as pbar:
		# Iterate over the time intervals
		for interval_start, interval_end in zip(
			time_intervals['time_interval'][:-1], time_intervals['time_interval'][1:]
		):
			# Filter the rows in times_df within the current time interval
			filtered_rows = times_df[
				(times_df['departure_time'] >= interval_start) & (times_df['departure_time'] < interval_end)
			]

			# Initialize a dictionary to store data for the current interval
			interval_data = {}

			# Iterate over the filtered rows
			for index, row in filtered_rows.iterrows():
				stop_id = row['stop_id']
				stop_info = stops_dict.get(stop_id)
				if stop_info:
					stop_lat = stop_info['stop_lat']
					stop_lon = stop_info['stop_lon']

					# Store the lat-lon pair for the stop
					interval_data[stop_id] = [stop_lat, stop_lon]

			# Store the data for the current interval
			quality_data[interval_start.strftime('%H:%M:%S')] = interval_data

			# Update the progress bar
			pbar.update(1)

		# Explicitly check and add the data for the last interval
		last_interval_data = {}
		last_interval_start = time_intervals['time_interval'].iloc[-1]
		filtered_rows = times_df[times_df['departure_time'] == last_interval_start]
		for index, row in filtered_rows.iterrows():
			stop_id = row['stop_id']
			stop_info = stops_dict.get(stop_id)
			if stop_info:
				stop_lat = stop_info['stop_lat']
				stop_lon = stop_info['stop_lon']
				last_interval_data[stop_id] = [stop_lat, stop_lon]
		if last_interval_data:
			quality_data[last_interval_start.strftime('%H:%M:%S')] = last_interval_data

	return quality_data


def explore_nested_dict(d, depth=0, level=1, length=False):
	if depth >= level:
		return
	for key, value in d.items():
		if isinstance(value, dict):
			message = "  " * depth + f"Key: {key}"
			if length:
				message += f" - Length: {len(value)}"
			print(message)
			explore_nested_dict(value, depth + 1, level)
		else:
			print("  " * depth + f" - Key: {key}")
			print("  " * (depth + 1) + f" - Value: {value}")
	if length:
		print(f"Length: {len(d)}")
