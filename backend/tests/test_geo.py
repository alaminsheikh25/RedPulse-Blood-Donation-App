import math

from app.utils.geo import haversine_km, within_radius


def test_haversine_same_point():
    assert haversine_km(0, 0, 0, 0) == 0.0


def test_haversine_known_distance():
    # Delhi to Mumbai ~1150 km
    d = haversine_km(28.6139, 77.2090, 19.0760, 72.8777)
    assert 1100 < d < 1200


def test_within_radius():
    assert within_radius(28.6, 77.2, 28.7, 77.3, 50)
    assert not within_radius(28.6, 77.2, 19.0, 72.8, 50)
    assert not within_radius(None, 77.2, 28.7, 77.3, 50)
