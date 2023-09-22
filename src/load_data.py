# loadData.py

import pandas as pd
import os
import pickle
from settings import gtfs_dir


def load_gtfs_data():
	print("\n1. Chargement des données...")

	# Load *.txt
	stops_df = pd.read_csv(os.path.join(gtfs_dir, "stops.txt"), usecols=['stop_code', 'stop_lat', 'stop_lon'])
	times_df = pd.read_csv(os.path.join(gtfs_dir, "stop_times.txt"), usecols=['stop_id', 'trip_id', 'departure_time'])
	routes_df = pd.read_csv(os.path.join(gtfs_dir, "routes.txt"), usecols=['route_id', 'route_type'])
	trips_df = pd.read_csv(os.path.join(gtfs_dir, "trips.txt"), usecols=['route_id', 'trip_id'])

	# extract bus stops and times
	bus_route_ids = routes_df[routes_df['route_type'] == 3]['route_id']
	bus_trips = trips_df[trips_df['route_id'].isin(bus_route_ids)]

	bus_departure_times = times_df[times_df['trip_id'].isin(bus_trips['trip_id'])]
	bus_departure_times = bus_departure_times[['stop_id', 'departure_time']]
	bus_departure_times = clean_times_data(bus_departure_times)

	bus_stops = stops_df[stops_df['stop_code'].isin(bus_departure_times['stop_id'])]
	bus_stops = bus_stops.rename(columns={'stop_code': 'stop_id'})
	bus_stops = clean_stops_data(bus_stops)

	return bus_departure_times, bus_stops


def clean_times_data(data_df):
	# Remove rows with missing departure and arrival times
	data_df = data_df.dropna(subset=['departure_time'])

	# Correct invalid departure times (e.g., replace '24:00:00' with '00:00:00')
	invalid_times = data_df['departure_time'].str.contains(r'^24:')
	data_df.loc[invalid_times, 'departure_time'] = data_df.loc[invalid_times, 'departure_time'].str.replace('24:', '00:')

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

	# Remove rows with invalid latitude and longitude values
	# data_df = data_df[(data_df['stop_lat'] >= -90) & (data_df['stop_lat'] <= 90)]

	# Remove rows with invalid latitude and longitude values
	# data_df = data_df[(data_df['stop_lon'] >= -180) & (data_df['stop_lon'] <= 180)]

	# remove duplicates
	data_df = data_df.drop_duplicates(subset=['stop_id'])

	# Reindex the DataFrame
	data_df = data_df.reset_index(drop=True)

	return data_df


def afficher_df(data_df, nom_df):
	print("\n=========================================================================================================")
	print(f"{nom_df}: {len(data_df)} rows")
	print(data_df.head(n=2).to_string())


def save_data(data, file_name='quality_data.pkl'):
	with open(f'resources/{file_name}.pkl', 'wb') as file:
		pickle.dump(data, file)


def load_data(file_name='quality_data.pkl'):
	with open(f'resources/{file_name}.pkl', 'rb') as file:
		data = pickle.load(file)
	return data
