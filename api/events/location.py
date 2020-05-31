import abc
from typing import Optional

from api.gravity.constructor import Location


class LocationFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch(self, location: str) -> Optional[Location]:
        pass
