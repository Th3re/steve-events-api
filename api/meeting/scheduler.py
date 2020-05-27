import abc
from typing import List


class Meeting:
    def __init__(self, summary: str, start: str, end: str, location: str, participants: List[str]):
        self.summary = summary
        self.start = start
        self.end = end
        self.location = location
        self.participants = participants


class Scheduler(abc.ABC):
    @abc.abstractmethod
    def schedule(self, token, meeting: Meeting):
        pass
