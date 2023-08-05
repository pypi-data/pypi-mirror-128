from datetime import datetime
from typing import Optional

import iso8601
from geopy import Point
from geopy.distance import Distance, geodesic


def parse_point(data) -> Optional[Point]:
    """Parse returned data into a ``Point`` object."""
    if data is None:
        return None
    else:
        return Point(data.get("lat"), data.get("lon"), data.get("alt"))


def parse_distance(value, unit='kilometers') -> Optional[Distance]:
    """Parse returned data into a ``Distance`` object."""
    if value is None:
        return None
    else:
        return geodesic(**{unit: value})


def parse_datetime(value) -> Optional[datetime]:
    """Parse returned data into a ``datetime`` object."""
    if value is None:
        return None
    else:
        return iso8601.parse_date(value)
