# 1. Collecte de données

import requests
import zipfile
import os

gtfs_url = "https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

download_dir = "data_gtfs"

if not os.path.exists(download_dir):
	os.makedirs(download_dir)

response = requests.get(gtfs_url)

if response.status_code == 200:
	zip_file_path = os.path.join(download_dir, "gtfs_stm.zip")
	with open(zip_file_path, "wb") as zip_file:
		zip_file.write(response.content)
	with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
		zip_ref.extractall(download_dir)
	print("Téléchargement et extraction réussis.")
else:
	print("Échec du téléchargement.")
