# Working with geospatial data in vector format (shapefile format)
# Project the data to a different CRS

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

sns.set_style("white")
sns.set(font_scale=1.5)

# Import the data
sjer_roads_path = os.path.join("spatial-vector-lidar", "california", 
                               "madera-county-roads", "tl_2013_06039_roads.shp")
sjer_roads = gpd.read_file(sjer_roads_path)

# aoi stands for area of interest
sjer_aoi_path = os.path.join("spatial-vector-lidar", "california", 
                             "neon-sjer-site", "vector_data", "SJER_crop.shp")
sjer_aoi = gpd.read_file(sjer_aoi_path)

# View the Coordinate Reference System of both layers 
print(sjer_roads.crs) # epsg:4269
print(sjer_aoi.crs) # epsg: 32611

# Reproject the aoi to match the roads layer
sjer_aoi_wgs84  = sjer_aoi.to_crs(epsg=4269)
# when you reproject the data, you specify the CRS that you wish to transform your data to
# you can also use the crs value from an object, such as: # sjer_aoi_wgs84  = sjer_aoi.to_crs(sjer_roads.crs)
# or you can use the full proj.4 string # sjer_aoi_wgs84  = sjer_aoi.to_crs("+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs ")

# Plot the data
fig, ax = plt.subplots(figsize=(12, 8))

sjer_roads.plot(cmap='Greys', ax=ax, alpha=.5)
sjer_aoi_wgs84.plot(ax=ax, markersize=10, color='r')

ax.set_title("Madera County Roads with SJER AOI");

plt.show()
