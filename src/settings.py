# settings.py

from matplotlib.colors import LinearSegmentedColormap

BUS_TYPE = 3

# Define the URL to download the GTFS data
GTFS_URL = "https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

# Define the paths to the GTFS files
GTFS_DIR = "resources/data_gtfs"
HEATMAP_IMAGES_DIR = "resources/heatmap/images"
DATA_FOLDER = "resources/heatmap/data"

# Define the latitude and longitude bounds
MIN_LATITUDE = 45.4
MAX_LATITUDE = 45.7
MIN_LONGITUDE = -73.9
MAX_LONGITUDE = -73.5

# Define the grid size in meters
GRID_SIZE = 100
LATITUDE_DEGREE_LENGTH = 111000
MAP_COLORS = [(0, 0, 0, 1), (0, 1, 0, 1), (1, 0, 0, 1)]
COLOR_MAP = LinearSegmentedColormap.from_list('colormap', MAP_COLORS)
FONT_COLOR = '#777'
