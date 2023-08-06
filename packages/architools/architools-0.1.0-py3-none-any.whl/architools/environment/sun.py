import datetime

from dateutil import tz, parser
from pysolar.solar import (
    get_altitude, 
    get_azimuth,
)
from pysolar.radiation import get_radiation_direct

def altitude(location, date):
    d = parser.isoparse(date)
    return get_altitude(location[0], location[1], d)

def azimuth(location, date):
    d = parser.isoparse(date)
    return get_azimuth(location[0], location[1], d)

def radiation(location, date):
    alt = altitude(location, date)
    d = parser.isoparse(date)
    result = get_radiation_direct(d, alt)
    return result
