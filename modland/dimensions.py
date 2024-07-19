# constants and formulas based on
# https://code.env.duke.edu/projects/mget/wiki/SinusoidalMODIS
# with slight modifications to boundaries based on proj4

# spherical earth radius (authalic radius)
EARTH_RADIUS_METERS = 6371007.181000

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

MODLAND_TILE_SIZES = {
    250: 4800,
    500: 2400,
    1000: 1200,
    5000: 240,
    10000: 120
}

# x coordinate of left side of sinusoidal target
# (upper-left corner of pixel)
def modland_left_x_meters(horizontal_index):
    if horizontal_index >= TOTAL_COLUMNS or horizontal_index < 0:
        raise IndexError('horizontal index (%d) out of bounds' % horizontal_index)

    return UPPER_LEFT_X_METERS + int(horizontal_index) * TILE_SIZE_METERS


# x coordinate of right side of right-most pixels of sinusoidal target
def modland_right_x_meters(horizontal_index):
    if horizontal_index >= TOTAL_COLUMNS or horizontal_index < 0:
        raise IndexError('horizontal (%d) index out of bounds' % horizontal_index)

    return modland_left_x_meters(horizontal_index) + TILE_SIZE_METERS



# y coordinate of top side of sinusoidal target
# (upper-left corner of pixel)
def modland_top_y_meters(vertical_index):
    if vertical_index >= TOTAL_ROWS or vertical_index < 0:
        raise IndexError('vertical index (%d) out of bounds' % vertical_index)

    return LOWER_RIGHT_Y_METERS + (TOTAL_ROWS - vertical_index) * TILE_SIZE_METERS


# y coordinate of the bottom side of bottom-most pixels of sinusoidal target
def modland_bottom_y_meters(vertical_index):
    if vertical_index >= TOTAL_ROWS or vertical_index < 0:
        raise IndexError('vertical index (%d) out of bounds' % vertical_index)

    return LOWER_RIGHT_Y_METERS + (TOTAL_ROWS - 1 - vertical_index) * TILE_SIZE_METERS


# size across each cell in meters given the number of cells across the target
def modland_cell_size_meters(cells_across_tile):
    return TILE_SIZE_METERS / cells_across_tile
