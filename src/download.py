# download.py

import requests
import zipfile
import os
from settings import gtfs_url, gtfs_dir


def download_gtfs_data():
	if not os.path.exists(gtfs_dir):
		os.makedirs(gtfs_dir)

	response = requests.get(gtfs_url)

	if response.status_code == 200:
		zip_file_path = os.path.join(gtfs_dir, "gtfs_stm.zip")
		with open(zip_file_path, "wb") as zip_file:
			zip_file.write(response.content)
		with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
			zip_ref.extractall(gtfs_dir)
		print("Téléchargement et extraction réussis.")
	else:
		print("Échec du téléchargement.")
