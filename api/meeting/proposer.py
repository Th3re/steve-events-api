import abc

from typing import List
from api.gravity.constructor import Location


class PlaceProposer(abc.ABC):
    @abc.abstractmethod
    def propose(self, location: Location) -> List[str]:
        pass
