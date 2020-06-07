import abc

from typing import Optional
from api.gravity.constructor import Location


class Place:
    def __init__(self, address, coordinates):
        self.address = address
        self.coordinates = coordinates

    def to_json(self):
        return {'address': self.address, 'coordinates': self.coordinates.to_json()}


class LocationFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch_geolocation(self, location: str) -> Optional[Location]:
        pass

    @abc.abstractmethod
    def fetch_place(self, location: Location) -> Optional[Place]:
        pass
