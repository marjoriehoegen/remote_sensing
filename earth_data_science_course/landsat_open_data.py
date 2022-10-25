# Read Landsat data, open all the bands and plot their histograms

import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import xarray as xr
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

# Create the path to your data
landsat_post_fire_path = os.path.join("cold-springs-fire", "landsat_collect", "LC080340322016072301T1-SC20180214145802", "crop")

# Generate a list of tif files
post_fire_paths = glob(os.path.join(landsat_post_fire_path,"*band*.tif"))

post_fire_paths.sort()
print(post_fire_paths)

# Open a single band using squeeze
band_1 = rxr.open_rasterio(post_fire_paths[0], masked=True).squeeze()
print(band_1.shape)

# Plot the data
f, ax=plt.subplots()
band_1.plot.imshow(ax=ax,cmap="Greys_r")

ax.set_axis_off()
ax.set_title("Plot of Band 1")
plt.show()

# Open all bands in a loop

def open_clean_bands(band_path):
    return rxr.open_rasterio(band_path, masked=True).squeeze()

all_bands = []
for i, aband in enumerate(post_fire_paths):
    all_bands.append(open_clean_bands(aband))
    # Assign a band number to the new xarray object
    all_bands[i]["band"]=i+1

# Turn list of bands into a single xarray object
landsat_post_fire_xr = xr.concat(all_bands, dim="band") 
print(landsat_post_fire_xr)

landsat_post_fire_xr.plot.imshow(col="band",col_wrap=3,cmap="Greys_r")
plt.show()

# Plot RGB image
ep.plot_rgb(landsat_post_fire_xr.values, rgb=[3, 2, 1], title="RGB Composite Image\n Post Fire Landsat Data")
plt.show()

ep.plot_rgb(landsat_post_fire_xr.values, rgb=[3, 2, 1], title="Landsat RGB Image\n Linear Stretch Applied", stretch=True, str_clip=4)
plt.show()

# Plot all band histograms using earthpy
band_titles = ["Band 1", 
               "Blue", 
               "Green", 
               "Red",
               "NIR", 
               "Band 6", 
               "Band7"]

ep.hist(landsat_post_fire_xr.values, title=band_titles)

plt.show()

# Color infrared image (CIR) using landsat bands: 4,3,2
ep.plot_rgb(landsat_post_fire_xr.values, rgb=[4, 3, 2], title="CIR Landsat Image Pre-Cold Springs Fire", figsize=(10, 10))
plt.show()
