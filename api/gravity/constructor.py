import abc
from typing import List, Optional


class Location:
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude


class Constructor(abc.ABC):
    @abc.abstractmethod
    def calculate(self, vertices: List[Location]) -> Optional[Location]:
        pass
