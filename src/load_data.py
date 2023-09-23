# loadData.py

import pandas as pd
import os
import pickle
from tqdm import tqdm
from settings import GTFS_DIR, DATA_FOLDER, MIN_LATITUDE, MIN_LONGITUDE, MAX_LATITUDE, MAX_LONGITUDE, BUS_TYPE


def load_gtfs_data():
	print("\n2. Traitement des données...")

	# Load *.txt
	stops_df = pd.read_csv(os.path.join(GTFS_DIR, "stops.txt"), usecols=['stop_code', 'stop_lat', 'stop_lon'])
	times_df = pd.read_csv(os.path.join(GTFS_DIR, "stop_times.txt"), usecols=['stop_id', 'trip_id', 'departure_time'])
	routes_df = pd.read_csv(os.path.join(GTFS_DIR, "routes.txt"), usecols=['route_id', 'route_type'])
	trips_df = pd.read_csv(os.path.join(GTFS_DIR, "trips.txt"), usecols=['route_id', 'trip_id'])

	stops_df = clean_stops_data(stops_df)

	# Extract bus stops and times
	bus_route_ids = routes_df[routes_df['route_type'] == BUS_TYPE]['route_id']
	bus_trips = trips_df[trips_df['route_id'].isin(bus_route_ids)]

	# Create a tqdm progress bar for loading data frames
	stop_times_iterator = tqdm(
		times_df[times_df['trip_id'].isin(bus_trips['trip_id'])][['stop_id', 'departure_time']]
		.iterrows(), total=len(bus_trips), desc="Loading Data", unit="rows", leave=False,
		position=0, dynamic_ncols=True
	)

	bus_departure_times = []
	for _, row in stop_times_iterator:
		bus_departure_times.append(row)
	bus_departure_times = pd.DataFrame(bus_departure_times, columns=['stop_id', 'departure_time'])

	bus_stops = stops_df[stops_df['stop_code'].isin(bus_departure_times['stop_id'])]
	bus_stops = bus_stops.rename(columns={'stop_code': 'stop_id'})

	# Clean data frames
	bus_departure_times = clean_times_data(bus_departure_times)
	bus_stops = clean_stops_data(bus_stops)

	return bus_departure_times, bus_stops


def clean_times_data(data_df):
	# Remove rows with missing departure and arrival times
	data_df = data_df.dropna(subset=['departure_time'])

	# Correct invalid departure times (e.g., replace '24:00:00' with '00:00:00')
	invalid_times = data_df['departure_time'].str.contains(r'^24:')
	data_df.loc[invalid_times, 'departure_time'] = (
		data_df.loc[invalid_times, 'departure_time'].str.replace('24:', '00:')
	)

	# Reindex the DataFrame
	data_df = data_df.reset_index(drop=True)

	# Convert departure times to datetime objects
	data_df['departure_time'] = pd.to_datetime(data_df['departure_time'], format='%H:%M:%S', errors='coerce').dt.time

	# Drop rows with invalid departure times
	data_df = data_df.dropna(subset=['departure_time'])

	# Reindex the DataFrame
	data_df = data_df.reset_index(drop=True)

	return data_df


def clean_stops_data(data_df):
	# Remove rows with missing latitude and longitude values
	data_df = data_df.dropna(subset=['stop_lat', 'stop_lon'])

	if 'stop_id' in data_df.columns:
		data_df = data_df.drop_duplicates(subset=['stop_id'])
	if 'stop_code' in data_df.columns:
		data_df = data_df.drop_duplicates(subset=['stop_code'])

	# Filter the stops based on latitude and longitude bounds
	data_df = data_df[
		(data_df['stop_lat'] >= MIN_LATITUDE) & (data_df['stop_lat'] <= MAX_LATITUDE) &
		(data_df['stop_lon'] >= MIN_LONGITUDE) & (data_df['stop_lon'] <= MAX_LONGITUDE)
	]

	# Reindex the DataFrame
	data_df = data_df.reset_index(drop=True)

	return data_df


def afficher_df(data_df, nom_df):
	print("\n=========================================================================================================")
	print(f"{nom_df}: {len(data_df)} rows")
	print(data_df.head(n=2).to_string())


def save_data(data, file_name='no_name_data'):
	os.makedirs(DATA_FOLDER, exist_ok=True)
	file_path = os.path.join(DATA_FOLDER, f'{file_name}.pkl')
	if os.path.exists(file_path):
		overwrite = input(
			f"The file '{file_name}' already exists. Do you want to overwrite it? (y/N): ").strip().lower()
		if overwrite != 'y':
			print("Data not saved.")
			return
	with open(file_path, 'wb') as file:
		pickle.dump(data, file)
	print(f"Data saved to '{file_name}'.")


def load_data(file_name='no_name_data'):
	file_path = os.path.join(DATA_FOLDER, f'{file_name}.pkl')
	if not os.path.exists(file_path):
		print(f"The file '{file_name}' does not exist.")
		return None
	with open(file_path, 'rb') as file:
		data = pickle.load(file)
	return data
