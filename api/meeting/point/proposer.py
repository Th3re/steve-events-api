import abc

from typing import List
from api.date.window import Window


class MeetingPointProposer(abc.ABC):
    @abc.abstractmethod
    def propose(self, window: Window, host: str, participants: List[str]) -> List[str]:
        pass
