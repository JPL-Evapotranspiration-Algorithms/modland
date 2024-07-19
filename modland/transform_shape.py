from typing import Union
import geopandas as gpd
from shapely.geometry.base import BaseGeometry

from .get_proj4 import get_proj4
from .projection import *

def transform_shape(
        shape: BaseGeometry,
        source_projection: Union[Proj, str],
        target_projection: Union[Proj, str]) -> BaseGeometry:
    if not isinstance(shape, BaseGeometry):
        raise ValueError("invalid shape")

    # TODO need to stop relying on deprecated proj4 as common projection encoding
    source_projection = get_proj4(source_projection)
    target_projection = get_proj4(target_projection)
    projected_shape = gpd.GeoDataFrame({}, geometry=[shape], crs=source_projection).to_crs(target_projection).geometry[
        0]

    return projected_shape

def transform_sinusoidal_to_latlon(shape: BaseGeometry) -> BaseGeometry:
    return transform_shape(shape, SINUSOIDAL, WGS84)

def transform_latlon_to_sinusoidal(shape: BaseGeometry) -> BaseGeometry:
    return transform_shape(shape, WGS84, SINUSOIDAL)
