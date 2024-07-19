from shapely.geometry import Polygon, MultiPolygon, Point, mapping

from .latlon_to_modland import latlon_to_modland
from .outlines import outline_latlon

# calculate MODIS land tiles intersecting a polygon in latitude and longitude
def find_modland_tiles(target_geometry_latlon, return_names=True, land_only=True):
    """
    Calculate MODIS land tiles intersecting a polygon in latitude and longitude.
    :param target_geometry_latlon: target polygon as a shapely geometry object with latitude and longitude coordinates
    :return: set of tuples of h and v indices of MODIS land tiles intersecting target polygon
    """

    # list of tiles intersecting target polygon
    intersecting_tiles = []

    # list of tiles at boundary coordinates of target polygon
    boundary_tiles = []

    # calculate target at each point in the target polygon

    if isinstance(target_geometry_latlon, Polygon):
        shapes = mapping(target_geometry_latlon)['coordinates']
    elif isinstance(target_geometry_latlon, MultiPolygon):
        shapes = mapping(target_geometry_latlon.convex_hull)['coordinates']
    elif isinstance(target_geometry_latlon, Point):
        shapes = [target_geometry_latlon]
    else:
        raise ValueError("unsupported target geometry: {}".format(target_geometry_latlon))

    # iterate through shapes
    for shape in shapes:

        if isinstance(shape, Point):
            shape = [shape]

        # iterate through coordinates
        for coordinate in shape:
            if isinstance(coordinate, Point):
                longitude = coordinate.x
                latitude = coordinate.y
            else:
                # pull latitude and longitude from coordinate
                longitude, latitude = coordinate

            # calculate target at coordinate
            tile = latlon_to_modland(latitude, longitude)

            # add target to list
            boundary_tiles += [tile]

    # set of tiles at boundary coordinates of target polygon
    boundary_tiles = set(boundary_tiles)

    # pull h and v indices from set of tiles
    horizontal_indices, vertical_indices = zip(*boundary_tiles)

    # iterate through range of horizontal indices
    for h in range(min(horizontal_indices), max(horizontal_indices) + 1):

        # iterate through range of vertical indices
        for v in range(min(vertical_indices), max(vertical_indices) + 1):
            polygon = outline_latlon(h, v)

            # check if target intersects target polygon
            if polygon.intersects(target_geometry_latlon):
                # add target to list
                intersecting_tiles += [(h, v)]

    # set of tiles intersecting target polygon
    intersecting_tiles = set(intersecting_tiles)

    if return_names:
        return sorted(["h{:02d}v{:02d}".format(h, v) for h, v in intersecting_tiles])
    else:
        return intersecting_tiles
