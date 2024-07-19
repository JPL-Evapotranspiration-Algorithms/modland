from .MODIS_land_tile import MODISLandTile

# calculate polygon outline of MODIS land target in sinusoidal coordinates
def outline_sinusoidal(h, v):
    """
    Calculate polygon outline of MODIS land target in sinusoidal coordinates.
    :param h: horizontal index of MODIS land target
    :param v: vertical index of MODIS land target
    :return: shapely geometry object containing polygon outline of MODIS land target in sinusoidal coordinates
    """
    return MODISLandTile(h, v, 100, 100).outline_sinusoidal()


# calculate polygon outline of MODIS land target in latitude and longitude
def outline_latlon(h, v):
    """
    Calculate polygon outline of MODIS land target in latitude and longitude.
    :param h: horizontal index of MODIS land target
    :param v: vertical index of MODIS land target
    :return: shapely geometry object containing polygon outline of MODIS land target in latitude and longitude
    """
    return MODISLandTile(h, v, 100, 100).outline_latlon
