import logging

import numpy as np
import rasters as rt
from rasters import Raster, RasterGeometry

from .find_modland_tiles import find_modland_tiles
from .modland_affine import *


def calculate_global_modland_indices(h, v, tile_size):
    global_modis_affine = calculate_modland_affine(0, 0, tile_size)
    affine = calculate_modland_affine(h, v, tile_size)
    tile_col_indices, tile_row_indices = np.meshgrid(np.arange(tile_size), np.arange(tile_size))
    x, y = affine * (tile_col_indices, tile_row_indices)
    global_col_indices, global_row_indices = ~global_modis_affine * (x, y)

    return global_row_indices, global_col_indices

def calculate_global_modland_serial_indices_hv(h, v, tile_size):
    global_row_indices, global_col_indices = calculate_global_modland_indices(h, v, tile_size)
    serial_index = global_row_indices * tile_size * 36 + global_col_indices
    serial_index = np.int32(serial_index)
    grid = generate_modland_grid(h, v, serial_index.shape[0])
    raster = Raster(serial_index, geometry=grid)

    return raster

def calculate_global_modland_serial_indices(tile, tile_size):
    h = int(tile[1:3])
    v = int(tile[4:6])
    indices = calculate_global_modland_serial_indices_hv(h, v, tile_size)

    return indices

def generate_modland_500m(fine_geometry: RasterGeometry, coarse_resolution: int = None) -> Raster:
    logger = logging.getLogger(__name__)

    FILL_VALUE = -9999
    DEFAULT_COARSE_RESOLUTION = 490

    if coarse_resolution is None:
        coarse_resolution = DEFAULT_COARSE_RESOLUTION

    tiles = find_modland_tiles(fine_geometry.boundary_latlon, return_names=True)
    geometry500m = fine_geometry.rescale(coarse_resolution)
    indices500m = np.full(geometry500m.shape, FILL_VALUE, dtype=np.int32)

    for tile in tiles:
        native_indices = calculate_global_modland_serial_indices(tile, 2400)
        coarse_indices = native_indices.to_geometry(geometry500m, nodata=FILL_VALUE)
        indices500m = rt.where(indices500m == FILL_VALUE, coarse_indices, indices500m)

    if np.any(indices500m == FILL_VALUE):
        unfilled_proportion = np.count_nonzero(indices500m == FILL_VALUE) / indices500m.size
        logger.warning(f"{round(unfilled_proportion * 100):0.2f} of fine pixels left unfilled")

    indices500m.nodata = FILL_VALUE

    return indices500m

def generate_modland_1000m(fine_geometry: RasterGeometry, coarse_resolution: int = None) -> Raster:
    logger = logging.getLogger(__name__)

    FILL_VALUE = -9999
    DEFAULT_COARSE_RESOLUTION = 980

    if coarse_resolution is None:
        coarse_resolution = DEFAULT_COARSE_RESOLUTION

    tiles = find_modland_tiles(fine_geometry.boundary_latlon, return_names=True)
    geometry = fine_geometry.rescale(coarse_resolution)
    indices = np.full(geometry.shape, FILL_VALUE, dtype=np.int32)

    for tile in tiles:
        native_indices = calculate_global_modland_serial_indices(tile, 1200)
        coarse_indices = native_indices.to_geometry(geometry, nodata=FILL_VALUE)
        indices = rt.where(indices == FILL_VALUE, coarse_indices, indices)

    if np.any(indices == FILL_VALUE):
        unfilled_proportion = np.count_nonzero(indices == FILL_VALUE) / indices.size
        logger.warning(f"{round(unfilled_proportion * 100):0.2f} of fine pixels left unfilled")

    indices.nodata = FILL_VALUE

    return indices

def calculate_global_modland_columns(spatial_resolution):
    tile_size = MODLAND_TILE_SIZES[spatial_resolution]
    global_modland_columns = tile_size * 36

    return global_modland_columns

def generate_modland_indices(geometry: RasterGeometry, spatial_resolution: float) -> Raster:
    x, y = geometry.get_xy(projection=SINUSOIDAL_PROJECTION)
    global_modland_affine = calculate_global_modland_affine(spatial_resolution)
    global_col_indices, global_row_indices = ~global_modland_affine * (x, y)
    global_col_indices = global_col_indices.astype(np.int32)
    global_row_indices = global_row_indices.astype(np.int32)
    global_modland_columns = calculate_global_modland_columns(spatial_resolution)
    serial_index = global_row_indices * global_modland_columns + global_col_indices
    serial_index = serial_index.astype(np.int32)
    serial_index = Raster(serial_index, geometry=geometry)

    return serial_index
