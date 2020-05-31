import abc
from datetime import datetime

from typing import List, Optional

from api.libs.events.event import Event


class ParticipantEvents:
    def __init__(self, participant: str, events: List[Event]):
        self.participant = participant
        self.events = events


class Fetcher(abc.ABC):
    @abc.abstractmethod
    def fetch(self, user_id: str) -> ParticipantEvents:
        pass

    @abc.abstractmethod
    def fetch_by_date(self, user_id: str, date: datetime) -> ParticipantEvents:
        pass
    
    @abc.abstractmethod
    def get_previous_event(self, user_id: str, date: datetime) -> Optional[Event]:
        pass
