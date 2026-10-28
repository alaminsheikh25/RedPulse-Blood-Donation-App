from __future__ import annotations

import math
from typing import Optional, Tuple

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    rlat1, rlon1, rlat2, rlon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    delta_lat = radius_km / 111.0
    delta_lon = radius_km / (111.0 * max(math.cos(math.radians(lat)), 1e-6))
    return lat - delta_lat, lat + delta_lat, lon - delta_lon, lon + delta_lon


def within_radius(lat1: Optional[float], lon1: Optional[float], lat2: Optional[float], lon2: Optional[float], radius_km: float) -> bool:
    if None in (lat1, lon1, lat2, lon2):
        return False
    return haversine_km(lat1, lon1, lat2, lon2) <= radius_km
