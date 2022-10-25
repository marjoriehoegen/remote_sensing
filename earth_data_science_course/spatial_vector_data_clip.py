# Working with geospatial data in vector format (shapefile format)
# Clip the data

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import geopandas as gpd

from shapely.geometry import box
import seaborn as sns

# Ignore warning about missing/empty geometries
import warnings
warnings.filterwarnings('ignore', 'GeoSeries.notna', UserWarning)

# Adjust plot font sizes
sns.set(font_scale=1.5)
sns.set_style("white")

# Import the data
country_boundary_us_path = os.path.join("spatial-vector-lidar", 
                                        "usa", "usa-boundary-dissolved.shp")
country_boundary_us = gpd.read_file(country_boundary_us_path)

state_boundary_us_path = os.path.join("spatial-vector-lidar", 
                                      "usa", "usa-states-census-2014.shp")
state_boundary_us = gpd.read_file(state_boundary_us_path)

pop_places_path = os.path.join("spatial-vector-lidar", "global", 
                               "ne_110m_populated_places_simple", "ne_110m_populated_places_simple.shp")
pop_places = gpd.read_file(pop_places_path)

# Check if they are in the same CRS
print("country_boundary_us", country_boundary_us.crs)
print("state_boundary_us", state_boundary_us.crs)
print("pop_places", pop_places.crs)

# Plot the data
fig, ax = plt.subplots(figsize=(12, 8))

country_boundary_us.plot(alpha=.5,ax=ax)

state_boundary_us.plot(cmap='Greys', ax=ax, alpha=.5)
pop_places.plot(ax=ax)

plt.axis('equal')
ax.set_axis_off()
# plt.show()

# Clip the data using GeoPandas clip
points_clip = gpd.clip(pop_places, country_boundary_us)

# View the first 6 rows and a few select columns
print(points_clip[['name', 'geometry', 'scalerank', 'natscale', ]].head())

# Plot the clipped data
fig, ax = plt.subplots(figsize=(12, 8))

country_boundary_us.plot(alpha=1, color="white", edgecolor="black", ax=ax)
state_boundary_us.plot(cmap='Greys', ax=ax, alpha=.5)
points_clip.plot(ax=ax,column='name')
ax.set_axis_off()
plt.axis('equal')


plt.show()
