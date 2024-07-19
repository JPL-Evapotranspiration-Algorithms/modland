"""
This module handles georeferencing MODIS land tiles.
"""
# rotation in affine transformation is not supported
# latitude and longitude are in WGS84 geographic coordinate system
import warnings
import geopandas as gpd
import numpy as np
import pyproj
import rasterio
from affine import Affine
from numpy import where, nan, isnan, all
from pyproj import Proj
from scipy.spatial.qhull import ConvexHull
from shapely.geometry import Polygon, Point, MultiPolygon
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import LinearRing

from .constants import *
from .projection import *
from .dimensions import *
from .get_proj4 import get_proj4
from .transform_shape import *
from .latlon_to_sinusoidal import latlon_to_sinusoidal
from .sinusoidal_to_latlon import sinusoidal_to_latlon
from .sinusoidal_to_modland import sinusoidal_to_modland
from .latlon_to_modland import latlon_to_modland
from .MODIS_land_tile import MODISLandTile
from .modland_pixels import *
from .outlines import *
from .find_modland_tiles import find_modland_tiles
from .modland_affine import *
from .parsehv import parsehv
from .indices import *

__author__ = 'Gregory H. Halverson'
