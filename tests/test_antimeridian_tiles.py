import numpy as np
from shapely.geometry import Polygon, box

from modland import MODISLandTile, find_modland_tiles, outline_latlon, outline_sinusoidal


def test_sinusoidal_matrices():
    tile = MODISLandTile(10, 5, 10, 10)
    x_mat, y_mat, lon_mat, lat_mat = tile.sinusoidal_matrices()
    assert x_mat.shape == (10, 10)
    assert y_mat.shape == (10, 10)
    assert not np.all(np.isnan(lon_mat))
    assert not np.all(np.isnan(lat_mat))


def test_antimeridian_boundary_tiles():
    # Boundary tiles straddling the sinusoidal projection limb (partial NaNs + valid pixels)
    for h, v in [(4, 4), (31, 4), (0, 8), (35, 8), (0, 9), (35, 9)]:
        tile = MODISLandTile(h, v, 100, 100)
        x_mat, y_mat, lon_mat, lat_mat = tile.sinusoidal_matrices()
        assert x_mat.shape == (100, 100)
        assert not np.all(np.isnan(x_mat))
        assert np.any(np.isnan(x_mat))

        sin_poly = tile.outline_sinusoidal
        assert isinstance(sin_poly, Polygon)
        assert sin_poly.is_valid
        assert sin_poly.area > 0

        ll_poly = tile.outline_latlon
        assert isinstance(ll_poly, Polygon)
        assert ll_poly.area > 0


def test_outline_helper_functions():
    sin_poly = outline_sinusoidal(10, 5)
    ll_poly = outline_latlon(10, 5)
    assert isinstance(sin_poly, Polygon)
    assert isinstance(ll_poly, Polygon)


def test_find_modland_tiles_56una():
    # Approximate WGS84 bounding box for MGRS tile 56UNA (near antimeridian / Bering Sea / Kamchatka)
    geom_56una = box(153.0, 54.0, 155.0, 55.1)
    tiles = find_modland_tiles(geom_56una, return_names=True)
    assert isinstance(tiles, list)
    assert len(tiles) > 0