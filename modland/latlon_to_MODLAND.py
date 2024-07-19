from .sinusoidal_to_modland import sinusoidal_to_modland
from .latlon_to_sinusoidal import latlon_to_sinusoidal

# MODIS land target indices for target containing latitude and longitude
def latlon_to_modland(latitude, longitude):
    if latitude < -90 or latitude > 90:
        raise ValueError('latitude (%f) out of bounds' % latitude)

    if longitude < -180 or longitude > 180:
        raise ValueError('longitude (%f) out of bounds' % longitude)

    return sinusoidal_to_modland(*latlon_to_sinusoidal(latitude, longitude))
