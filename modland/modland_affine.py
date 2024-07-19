from affine import Affine

from rasters import RasterGrid

from .projection import *
from .dimensions import MODLAND_TILE_SIZES

def calculate_modland_affine(h, v, tile_size):
    # boundaries of sinusodial projection
    UPPER_LEFT_X_METERS = -20015109.355798
    UPPER_LEFT_Y_METERS = 10007554.677899
    LOWER_RIGHT_X_METERS = 20015109.355798
    LOWER_RIGHT_Y_METERS = -10007554.677899

    # size across (width or height) of any equal-area sinusoidal target
    TILE_SIZE_METERS = 1111950.5197665554

    # boundaries of MODIS land grid
    TOTAL_ROWS = 18
    TOTAL_COLUMNS = 36

    y_max = LOWER_RIGHT_Y_METERS + (TOTAL_ROWS - v) * TILE_SIZE_METERS
    x_min = UPPER_LEFT_X_METERS + int(h) * TILE_SIZE_METERS

    cell_size = TILE_SIZE_METERS / tile_size

    # width of pixel
    a = cell_size
    # row rotation
    b = 0.0
    # x-coordinate of upper-left corner of upper-left pixel
    c = x_min
    # column rotation
    d = 0.0
    # height of pixel
    e = -1.0 * cell_size
    # y-coordinate of the upper-left corner of upper-left pixel
    f = y_max
    affine = Affine(a, b, c, d, e, f)

    return affine

def calculate_global_modland_affine(spatial_resolution):
    tile_size = MODLAND_TILE_SIZES[spatial_resolution]
    affine = calculate_modland_affine(0, 0, tile_size)

    return affine

def generate_modland_grid(h, v, tile_size):
    affine = calculate_modland_affine(h, v, tile_size)
    grid = RasterGrid.from_affine(affine, tile_size, tile_size, crs=SINUSOIDAL_PROJECTION)

    return grid
