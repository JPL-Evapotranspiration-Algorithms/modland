from .dimensions import *

# MODIS land target indices for target containing sinusoidal coordinate
def sinusoidal_to_modland(x_sinusoidal, y_sinusoidal):
    if x_sinusoidal < UPPER_LEFT_X_METERS or x_sinusoidal > LOWER_RIGHT_X_METERS:
        raise ValueError('sinusoidal x coordinate (%f) out of bounds' % x_sinusoidal)

    if y_sinusoidal < LOWER_RIGHT_Y_METERS or y_sinusoidal > UPPER_LEFT_Y_METERS:
        raise ValueError('sinusoidal y (%f) coordinate out of bounds' % y_sinusoidal)

    horizontal_index = int((x_sinusoidal - UPPER_LEFT_X_METERS) / TILE_SIZE_METERS)
    vertical_index = int((-1 * (y_sinusoidal + LOWER_RIGHT_Y_METERS)) / TILE_SIZE_METERS)

    if horizontal_index == TOTAL_COLUMNS:
        horizontal_index -= 1

    if vertical_index == TOTAL_ROWS:
        vertical_index -= 1

    return horizontal_index, vertical_index
