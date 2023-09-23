# download.py

import requests
import zipfile
import os
from settings import GTFS_URL, GTFS_DIR


def download_gtfs_data():
	print("\n1. Téléchargement des données...")
	if not os.path.exists(GTFS_DIR):
		os.makedirs(GTFS_DIR)

	response = requests.get(GTFS_URL)

	if response.status_code == 200:
		zip_file_path = os.path.join(GTFS_DIR, "gtfs_stm.zip")
		with open(zip_file_path, "wb") as zip_file:
			zip_file.write(response.content)
		with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
			zip_ref.extractall(GTFS_DIR)
		print("Téléchargement et extraction réussis.")
	else:
		print("Échec du téléchargement.")
