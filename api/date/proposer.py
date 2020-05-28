import abc
from datetime import datetime

from typing import List

from api.date.window import Window


class Proposer(abc.ABC):
    @abc.abstractmethod
    def propose(self, date: datetime, participants: List[str]) -> List[Window]:
        pass
