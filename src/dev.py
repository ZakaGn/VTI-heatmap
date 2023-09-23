# dev.py

from load_data import load_gtfs_data, afficher_df, save_data, load_data
from quality_of_service import explore_nested_dict, quality_of_service
from heatmaps import generate_heatmap_animation
from src.download import download_gtfs_data

# Téléchargement des donnees
download_gtfs_data()

# Chargement des donnees et sauvegarde
times_df, stops_df = load_gtfs_data()
save_data(times_df, "times_df")
save_data(stops_df, "stops_df")

# Generation de qualité de service
times_df = load_data("times_df")
stops_df = load_data("stops_df")
quality_data = quality_of_service(times_df, stops_df)
save_data(quality_data, "quality_data")

# Generation de heatmaps
quality_data = load_data("quality_data")
generate_heatmap_animation(quality_data)

# Affichage une version bref des données
# afficher_df(times_df, "times_df")
# afficher_df(stops_df, "stops_df")
# explore_nested_dict(quality_data, level=2, length=True)

print("Done.")
