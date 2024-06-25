from typing import Union
import warnings
import pyproj
from pyproj import Proj
import rasterio

def get_proj4(projection: Union[Proj, str]) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if isinstance(projection, Proj):
            result = projection.crs.to_proj4()

        elif isinstance(projection, rasterio.crs.CRS):
            result = projection.to_proj4()

        elif isinstance(projection, pyproj.crs.crs.CRS):
            result = projection.to_proj4()

        elif isinstance(projection, str):
            # result = pycrs.parse.from_unknown_text(projection).to_proj4()
            result = pyproj.CRS(projection).to_proj4()

        else:
            raise ValueError(f"projection not recognized ({type(projection)})")

    result = result.replace("+shell=epsg:", "epsg:")

    return result
