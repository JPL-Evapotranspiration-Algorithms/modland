from pyproj import Proj

MODIS_LAND_TILE_PROJECTION_WKT = 'PROJCS["unnamed",GEOGCS["Unknown datum based upon the custom spheroid",DATUM["Not_specified_based_on_custom_spheroid",SPHEROID["Custom spheroid",6371007.181,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Sinusoidal"],PARAMETER["longitude_of_center",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'
MODIS_LAND_TILE_PROJECTION_PROJ4 = '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs'
MODIS_LAND_TILE_PROJECTION_PCI = ['SIN         E700', 'METRE',
                                  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]
MODIS_LAND_TILE_PROJECTION_MI = 'Earth Projection 16, 104, "m", 0'
MODIS_LAND_TILE_PROJECTION_EPSG = 6842

SINUSOIDAL = Proj(MODIS_LAND_TILE_PROJECTION_PROJ4)
WGS84 = Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ')

SINUSOIDAL_PROJECTION = "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"
