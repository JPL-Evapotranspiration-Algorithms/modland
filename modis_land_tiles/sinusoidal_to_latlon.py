from .projection import SINUSOIDAL
from .dimensions import *

# transforms sinusoidal coordinates in meters to WGS84 latitude and longitude
def sinusoidal_to_latlon(x_sinusoidal, y_sinusoidal):
    if x_sinusoidal < UPPER_LEFT_X_METERS or x_sinusoidal > LOWER_RIGHT_X_METERS:
        raise ValueError('sinusoidal x coordinate (%f) out of bounds' % x_sinusoidal)

    if y_sinusoidal < LOWER_RIGHT_Y_METERS or y_sinusoidal > UPPER_LEFT_Y_METERS:
        raise ValueError('sinusoidal y (%f) coordinate out of bounds' % y_sinusoidal)

    longitude, latitude = SINUSOIDAL(x_sinusoidal, y_sinusoidal, inverse=True)

    if x_sinusoidal < 0 and x_sinusoidal < SINUSOIDAL(-180, latitude)[0]:
        return None, None

    if x_sinusoidal > 0 and x_sinusoidal > SINUSOIDAL(180, latitude)[0]:
        return None, None

    return latitude, longitude
