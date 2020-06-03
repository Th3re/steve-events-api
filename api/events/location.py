import abc

from typing import Optional
from api.gravity.constructor import Location


class Place:
    def __init__(self, address):
        self.address = address


class LocationFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch_geolocation(self, location: str) -> Optional[Location]:
        pass

    @abc.abstractmethod
    def fetch_place(self, location: Location) -> Optional[Place]:
        pass
