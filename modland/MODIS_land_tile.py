import numpy as np
from affine import Affine
from scipy.spatial.qhull import ConvexHull
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing

from .constants import *
from .dimensions import *
from .latlon_to_sinusoidal import latlon_to_sinusoidal
from .sinusoidal_to_latlon import sinusoidal_to_latlon
from .sinusoidal_to_modland import sinusoidal_to_modland
from .transform_shape import *

# encapsulation of MODIS land target at given indices
# affine transform of raster can be calculated given count of rows and columns
class MODISLandTile:
    def __init__(self, horizontal_index, vertical_index, rows, columns):

        if horizontal_index >= TOTAL_COLUMNS or horizontal_index < 0:
            raise IndexError('horizontal index (%d) out of bounds' % horizontal_index)

        if vertical_index >= TOTAL_ROWS or vertical_index < 0:
            raise IndexError('vertical index (%d) out of bounds' % vertical_index)

        if rows < 0:
            raise ValueError('rows cannot be negative (%d)' % rows)

        if columns < 0:
            raise ValueError('columns cannot be negative (%d)' % columns)

        self.horizontal_index = horizontal_index
        self.vertical_index = vertical_index
        self.rows = rows
        self.columns = columns

    def __str__(self):
        return "<MODISLandTile h%02dv%02d, rows: %d, columns: %d>" \
               % (self.horizontal_index, self.vertical_index, self.rows, self.columns)

    # x coordinate of left side of sinusoidal target
    # (upper-left corner of pixel)
    @property
    def x_min(self):
        return modland_left_x_meters(self.horizontal_index)

    # x coordinate of center of upper-left pixel
    @property
    def x_min_center(self):
        return self.x_min + self.cell_width_meters / 2.0

    # x coordinate of right side right-most pixels of sinusoidal target
    @property
    def x_max(self):
        return modland_right_x_meters(self.horizontal_index)

    # y coordinate of top side of sinusoidal target
    # (upper-left corner of pixel)
    @property
    def y_max(self):
        return modland_top_y_meters(self.vertical_index)

    # y coordinate of center of upper-left pixel
    @property
    def y_max_center(self):
        return self.y_max - self.cell_height_meters / 2.0

    # y coordinate of the bottom side of bottom-most pixels of sinusoidal target
    @property
    def y_min(self):
        return modland_bottom_y_meters(self.vertical_index)

    # width of cell in meters given number of columns
    @property
    def cell_width_meters(self):
        return modland_cell_size_meters(self.columns)

    # positive height of cell in meters given number of rows
    @property
    def cell_height_meters(self):
        return modland_cell_size_meters(self.rows)

    # tuple of cell width and height
    @property
    def cell_size_meters(self):
        return (self.cell_width_meters, self.cell_height_meters)

    # affine transform (as tuple) of target given cells across target
    @property
    def affine_tuple(self):

        # width of pixel
        a = self.cell_width_meters

        # row rotation
        b = 0.0

        # x-coordinate of upper-left corner of upper-left pixel
        c = self.x_min

        # column rotation
        d = 0.0

        # height of pixel
        e = -1.0 * self.cell_height_meters

        # y-coordinate of the upper-left corner of upper-left pixel
        f = self.y_max

        affine_transform = (a, b, c, d, e, f)

        return affine_transform

    # affine transform as affine.Affine
    @property
    def affine_transform(self):
        return Affine(*self.affine_tuple)

    @property
    def affine_center(self):
        return self.affine_transform * Affine.translation(0.5, 0.5)

    # affine transform as tuple in ESRI world format
    @property
    def affine_esri(self):

        # width of pixel
        a = self.cell_width_meters

        # column rotation
        d = 0.0

        # row rotation
        b = 0.0

        # height of pixel
        e = -1.0 * self.cell_height_meters

        # x coordinate of center of upper-left pixel
        c = self.x_min_center

        # y coordinate of center of upper-left pixel
        f = self.y_max_center

        affine_transform = (a, d, b, e, c, f)

        return affine_transform

    # save esri world file for target
    def save_world_file(self, filename):
        with open(filename, 'w') as f:
            f.write('\n'.join([str(parameter) for parameter in (self.affine_esri)]))

    # affine transform as tuple in GDAL format
    @property
    def affine_gdal(self):

        # x-coordinate of upper-left corner of upper-left pixel
        c = self.x_min

        # width of pixel
        a = self.cell_width_meters

        # row rotation
        b = 0.0

        # y-coordinate of the upper-left corner of upper-left pixel
        f = self.y_max

        # column rotation
        d = 0.0

        # height of pixel
        e = -1.0 * self.cell_height_meters

        affine_transform = (c, a, b, f, d, e)

        return affine_transform

    # x, y sinusoidal coordinate in meters from row and column
    # top left of pixel if center is set to False
    # center of pixel if center is set to True
    def sinusoidal(self, row, column, center=CENTER_PIXEL_COORDINATES_DEFAULT):
        if row >= self.rows or row < 0:
            raise IndexError('row (%d) out of bounds' % row)

        if column >= self.columns or column < 0:
            raise IndexError('column (%d) out of bounds' % column)

        # top-left corner coordinates of pixel
        x_sinusoidal, y_sinusoidal = self.affine_transform * (column, row)

        # offset coordinates to center of pixel
        if center:
            x_sinusoidal += self.cell_width_meters / 2.0
            y_sinusoidal -= self.cell_height_meters / 2.0

        return (x_sinusoidal, y_sinusoidal)

    # get row and column of cell at sinusoidal coordinates
    def row_column_from_sinusoidal(self, x_sinusoidal, y_sinusoidal):
        if x_sinusoidal < self.x_min or x_sinusoidal >= self.x_max:
            raise ValueError('sinusoidal x coordinate (%f) out of bounds' % x_sinusoidal)

        if y_sinusoidal <= self.y_min or y_sinusoidal > self.y_max:
            raise ValueError('sinusoidal y (%f) coordinate out of bounds' % y_sinusoidal)

        return tuple([int(index)
                      for index
                      in ~(self.affine_transform) * (x_sinusoidal, y_sinusoidal)])

    def row_column_from_latlon(self, latitude, longitude):
        return self.row_column_from_sinusoidal(*latlon_to_sinusoidal(latitude, longitude))

    # get latitude and longitude of cell at row and column
    # top left of pixel if center is set to False
    # center of pixel if center is set to True
    def latlon(self, row, column, center=CENTER_PIXEL_COORDINATES_DEFAULT):
        if row >= self.rows or row < 0:
            raise IndexError('row (%d) out of bounds' % row)

        if column >= self.columns or column < 0:
            raise IndexError('column (%d) out of bounds' % column)

        latitude, longitude = sinusoidal_to_latlon(*self.sinusoidal(row, column, center=center))

        return (latitude, longitude)

    # latitude matrix and longitude matrix for coordinates of each cell in target
    # top left of pixel if center is set to False
    # center of pixel if center is set to True
    def latlon_matrices(self, center=CENTER_PIXEL_COORDINATES_DEFAULT):
        # lon, lat = sinusoidal_projection(*self.sinusoidal_matrices(center=center), inverse=True)
        _, _, lon, lat = self.sinusoidal_matrices(center=center)

        return lat, lon

    # sinusoidal x and y matrices of each cell in target
    # top left of pixel if center is set to False
    # center of pixel if center is set to True
    def sinusoidal_matrices(self, center=CENTER_PIXEL_COORDINATES_DEFAULT):

        if center:
            affine = self.affine_center
        else:
            affine = self.affine_transform

        x_matrix, y_matrix = np.meshgrid(np.arange(self.columns), np.arange(self.rows)) * affine
        lon, lat = SINUSOIDAL(x_matrix, y_matrix, inverse=True)

        if self.horizontal_index < 18:
            valid = lon < 0
        else:
            valid = lon >= 0

        x_matrix = np.where(valid, x_matrix, np.nan)
        y_matrix = np.where(valid, y_matrix, np.nan)
        lon = np.where(valid, lon, np.nan)
        lat = np.where(valid, lat, np.nan)

        return x_matrix, y_matrix, lon, lat

    # checks if a sinusoidal coordinate falls within the target
    def contains_sinusoidal(self, x_sinusoidal, y_sinusoidal):
        if x_sinusoidal < UPPER_LEFT_X_METERS or x_sinusoidal > LOWER_RIGHT_X_METERS:
            raise ValueError('sinusoidal x coordinate (%f) out of bounds' % x_sinusoidal)

        if y_sinusoidal < LOWER_RIGHT_Y_METERS or y_sinusoidal > UPPER_LEFT_Y_METERS:
            raise ValueError('sinusoidal y (%f) coordinate out of bounds' % y_sinusoidal)

        h, v = sinusoidal_to_modland(x_sinusoidal, y_sinusoidal)

        return h == self.horizontal_index and v == self.vertical_index

    # checks if a latitude and longitude coordinate falls within the target
    def contains_latlon(self, latitude, longitude):
        return self.contains_sinusoidal(*latlon_to_sinusoidal(latitude, longitude))

    @property
    def outline_sinusoidal(self):
        upper_left_x = lower_left_x = self.x_min
        upper_right_x = lower_right_x = self.x_max
        upper_left_y = upper_right_y = self.y_max
        lower_left_y = lower_right_y = self.y_min

        # tests if corners exist
        upper_left_valid = any(sinusoidal_to_latlon(upper_left_x, upper_left_y))
        upper_right_valid = any(sinusoidal_to_latlon(upper_right_x, upper_right_y))
        lower_right_valid = any(sinusoidal_to_latlon(lower_right_x, lower_right_y))
        lower_left_valid = any(sinusoidal_to_latlon(lower_left_x, lower_left_y))

        # case where all corners exist
        if all([upper_left_valid, upper_right_valid, lower_right_valid, lower_left_valid]):
            return Polygon(LinearRing([
                [upper_left_x, upper_left_y],
                [upper_right_x, upper_right_y],
                [lower_right_x, lower_right_y],
                [lower_left_x, lower_left_y]
            ]))
        else:
            x_matrix, y_matrix, lon, lat = self.sinusoidal_matrices()
            points = np.dstack([x_matrix.flatten(), y_matrix.flatten()])[0]
            points = points[~all(np.isnan(points), axis=1)]
            hull = ConvexHull(points)
            vertices = hull.points[hull.vertices]
            poly = Polygon(vertices)
            return poly

    @property
    def outline_latlon(self):
        return transform_sinusoidal_to_latlon(self.outline_sinusoidal)

    @property
    def bounds_sinusoidal(self):
        return self.x_min, self.y_min, self.x_max, self.y_max
