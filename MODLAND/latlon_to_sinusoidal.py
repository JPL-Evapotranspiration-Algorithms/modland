from .projection import SINUSOIDAL

# transforms WGS84 latitude and longitude to sinusoidal coordinates in meters
def latlon_to_sinusoidal(latitude, longitude):
    if latitude < -90 or latitude > 90:
        raise ValueError('latitude (%f) out of bounds' % latitude)

    if longitude < -180 or longitude > 180:
        raise ValueError('longitude (%f) out of bounds' % longitude)

    return SINUSOIDAL(longitude, latitude)
