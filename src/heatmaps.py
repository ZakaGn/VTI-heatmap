import os
import shutil
import imageio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from settings import *


def generate_heatmap_animation(quality_data):
	print("\n4. Génération des heatmaps...")
	# Ensure the heatmap directory exists and is empty
	os.makedirs(HEATMAP_IMAGES_DIR, exist_ok=True)
	clear_directory(HEATMAP_IMAGES_DIR)

	# Use tqdm to create a progress bar for generating images
	for timestamp, data in tqdm(quality_data.items(), desc="Generating Heatmap Images"):
		# Generate the heatmap image for the current timestamp
		image_path = os.path.join(HEATMAP_IMAGES_DIR, f"heatmap_{timestamp}.png")
		generate_heatmap_image({timestamp: data}, image_path)

	# Create an animation from the generated images
	animation_output_path = os.path.join(HEATMAP_IMAGES_DIR, "heatmap_animation.gif")
	create_gif_from_images(animation_output_path)

	return animation_output_path


def generate_heatmap_image(timestamp_data, output_file):
	latitudes = np.arange(MIN_LATITUDE, MAX_LATITUDE, GRID_SIZE / LATITUDE_DEGREE_LENGTH)
	longitudes = np.arange(
		MIN_LONGITUDE, MAX_LONGITUDE, GRID_SIZE / (LATITUDE_DEGREE_LENGTH * np.radians(MIN_LATITUDE))
	)

	for timestamp, data in timestamp_data.items():
		quality_grid = np.zeros((len(latitudes), len(longitudes)))

		for stop_id, stop_info in data.items():
			if isinstance(stop_info, dict):
				latitude = stop_info.get('Latitude', 0)
				longitude = stop_info.get('Longitude', 0)
				stops = stop_info.get('stops', 0)
			else:
				latitude = 0
				longitude = 0
				stops = 0

			# Find the grid cell indices for the given latitude and longitude
			lat_idx = int((latitude - MIN_LATITUDE) / (GRID_SIZE / LATITUDE_DEGREE_LENGTH))
			lon_idx = int(
				(longitude - MIN_LONGITUDE) / (GRID_SIZE / (LATITUDE_DEGREE_LENGTH * np.radians(MIN_LATITUDE))))

			# Check if the indices are within the valid range of quality_grid
			if 0 <= lat_idx < quality_grid.shape[0] and 0 <= lon_idx < quality_grid.shape[1]:
				quality_grid[lat_idx, lon_idx] += stops

		# Create a heatmap using seaborn
		sns.set()
		plt.figure(figsize=(10, 8))
		fig = plt.figure(facecolor='black')
		ax = sns.heatmap(
			quality_grid,
			vmin=0,
			vmax=50,
			cmap=COLOR_MAP,
			cbar=True,
			cbar_kws={'label': 'Quality'}
		)

		ax.set_facecolor((0, 0, 0, 1))
		ax.set_xticks([])
		ax.set_yticks([])
		ax.set_xlabel("Longitude", color=FONT_COLOR)
		ax.set_ylabel("Latitude", color=FONT_COLOR)
		ax.set_title(f"Quality Heatmap at {timestamp}", color=FONT_COLOR)
		ax.tick_params(axis='x', colors=FONT_COLOR)
		ax.tick_params(axis='y', colors=FONT_COLOR)
		ax.invert_yaxis()

		plt.savefig(output_file, facecolor=fig.get_facecolor())
		plt.close('all')


def create_gif_from_images(output_file):
	images = []
	for filename in sorted(os.listdir(HEATMAP_IMAGES_DIR)):
		if filename.startswith("heatmap_") and filename.endswith(".png"):
			image_path = os.path.join(HEATMAP_IMAGES_DIR, filename)
			image = imageio.imread(image_path)
			images.append(image)
	imageio.mimsave(output_file, images, duration=0.5)


def clear_directory(directory):
	if os.path.exists(directory):
		for item in os.listdir(directory):
			item_path = os.path.join(directory, item)
			if os.path.isfile(item_path):
				os.remove(item_path)
			elif os.path.isdir(item_path):
				shutil.rmtree(item_path)
