# Process Landsat data from the Cold Springs fire, plot the pre and post fire image

import os
from glob import glob

import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio
import xarray as xr
import rioxarray as rxr
import numpy as np
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from shapely.geometry import mapping

###########################################################
# Goal: select red, green, blue and near infrared bands
###########################################################

# Landsat file naming convention
# LC080340322016072301T1-SC20180214145802
#L: Landsat Sensor
# C: OLI / TIRS combined platform
# 08: Landsat
# 034032: The next 6 digits represent the path and row of the scene. This identifies the spatial coverage of the scene
# 20160723: representing the year, month and day that the data were collected.

# Function to open, crop and clean the data
def open_clean_band(band_path, clip_extent, valid_range=None):
    """A function that opens a Landsat band as an (rio)xarray object

    Parameters
    ----------
    band_path : list
        A list of paths to the tif files that you wish to combine.

    clip_extent : geopandas geodataframe
        A geodataframe containing the clip extent of interest.

    valid_range : tuple (optional)
        The min and max valid range for the data. All pixels with values outside
        of this range will be masked.

    Returns
    -------
    An single xarray object with the Landsat band data.

    """

    try:
        clip_bound = clip_extent.geometry
    except Exception as err:
        print("Geodataframe object needed.")
        print(err)

    cleaned_band = rxr.open_rasterio(band_path, masked=True).rio.clip(clip_bound,from_disk=True).squeeze()

    # Only mask the data if a valid range tuple is provided
    if valid_range:
        mask = ((landsat_post_xr_clip < valid_range[0]) | (landsat_post_xr_clip > valid_range[1]))
        cleaned_band = landsat_post_xr_clip.where(~xr.where(mask, True, False))

    return cleaned_band

def process_bands(paths, crop_layer, stack=False):
    """
    Open, clean and crop a list of raster files using rioxarray.

    Parameters
    ----------
    paths : list
        A list of paths to raster files that could be stacked (of the same 
        resolution, crs and spatial extent).
    
    crop_layer : geodataframe
        A geodataframe containing the crop geometry that you wish to crop your
        data to.
        
    stack : boolean
        If True, return a stacked xarray object. If false will return a list
        of xarray objects.

    Returns
    -------
        Either a list of xarray objects or a stacked xarray object
    """

    all_bands = []
    for i, aband in enumerate(paths):
        cleaned = open_clean_band(aband, crop_layer)
        cleaned["band"] = i+1
        all_bands.append(cleaned)

    if stack:
        return xr.concat(all_bands, dim="band")
    else:
        return all_bands


# Set path
landsat_post_fire_path = os.path.join("cold-springs-fire", "landsat_collect", "LC080340322016072301T1-SC20180214145802", "crop")

# Select bands 2 to 5
# Band 2 - Blue
# Band 3 - Green
# Band 4 - Red
# Band 5 - Near infrared (NIR)
all_landsat_post_bands = glob(os.path.join(landsat_post_fire_path,"*band[2-5]*.tif"))

# Make sure the bands are ordered
all_landsat_post_bands.sort()
print(all_landsat_post_bands)

# Open up boundary extent using GeoPandas
fire_boundary_path = os.path.join("cold-springs-fire", "vector_layers", "fire-boundary-geomac", "co_cold_springs_20160711_2200_dd83.shp")
fire_boundary = gpd.read_file(fire_boundary_path)

# The crop extent shapefile and the Landsat data need to be in the same Coordinate Reference System (CRS)
# Get CRS of Landsat data
landsat_crs = es.crs_check(all_landsat_post_bands[0])

print("Landsat crs is:", landsat_crs)
print("Fire boundary crs", fire_boundary.crs)

# Reproject data to CRS of raster data
fire_boundary_utmz13 = fire_boundary.to_crs(landsat_crs)

# Process all bands
post_fire_stack = process_bands(all_landsat_post_bands, fire_boundary_utmz13, stack=True)

# Plot the final stacked data
post_fire_stack.plot.imshow(col="band", col_wrap=2, cmap="Greys_r") # imshow() display data as an image, i.e., on a 2D regular raster

# Plot using earthpy
band_titles = ["Blue Band", "Green Band", "Red Band", "NIR Band"]
ep.plot_bands(post_fire_stack, cols=2, figsize=(10,5), title=band_titles)

# RGB Plot
ep.plot_rgb(post_fire_stack, rgb=[2, 1, 0],figsize=(10,5), title="CIR Image Landsat Post Fire")

# Compare with the pre-fire data
landsat_pre_fire_path = os.path.join("cold-springs-fire", "landsat_collect", "LC080340322016070701T1-SC20180214145604", "crop")
all_landsat_pre_bands = glob(os.path.join(landsat_pre_fire_path,"*band[2-5]*.tif"))
all_landsat_pre_bands.sort()

pre_fire_stack = process_bands(all_landsat_pre_bands, fire_boundary_utmz13, stack=True)

# Plot the final stacked data
pre_fire_stack.plot.imshow(col="band", col_wrap=2, cmap="Greys_r") # imshow() display data as an image, i.e., on a 2D regular raster

# Plot using earthpy
ep.plot_bands(pre_fire_stack, cols=2, figsize=(10,5), title=band_titles)
ep.plot_rgb(pre_fire_stack, rgb=[2, 1, 0],figsize=(10,5), title="CIR Image Landsat Pre Fire")

plt.show()
