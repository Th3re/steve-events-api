from datetime import datetime
from typing import List

from api.date.proposer import Proposer
from api.date.window import Window
from api.libs.db.store import Store
from api.libs.events.event import Event


class ParticipantEvents:
    def __init__(self, participant: str, events: List[Event]):
        self.participant = participant
        self.events = events


class DateProposer(Proposer):
    def __init__(self, store: Store):
        self.store = store

    def _participants_events(self, participants: List[str]) -> List[ParticipantEvents]:
        return [
            ParticipantEvents(
                participant=user_id,
                events=list(map(lambda e: Event.from_dict(e), self.store.get(user_id)))
            )
            for user_id in participants
        ]

    def propose(self, date: datetime, participants: List[str]) -> List[Window]:
        participants_events = self._participants_events(participants)
        return [Window(start=datetime.now(), end=datetime.now())]
