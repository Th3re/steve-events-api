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

    def _participant_events(self, user_id: str, date: datetime) -> ParticipantEvents:
        events = [event for event in [Event.from_json(e) for e in self.store.get(user_id)]
                  if event.start_time.day == date.day or event.end_time.day == date.day]
        return ParticipantEvents(user_id, events)

    def _participants_events(self, participants: List[str], date: datetime) -> List[ParticipantEvents]:
        return [self._participant_events(user_id, date) for user_id in participants]

    @staticmethod
    def _map_events_to_windows(participant_events: List[ParticipantEvents]):
        all_windows = []
        for participant in participant_events:
            participant_windows = [Window(start=event.start_time, end=event.end_time) for event in participant.events]
            all_windows.extend(participant_windows)
        return all_windows

    def propose(self, date: datetime, participants: List[str]) -> List[Window]:
        participants_events = self._participants_events(participants, date)
        all_windows = self._map_events_to_windows(participants_events)
        merged_windows = Window.merged(all_windows)
        initial_window = Window.initial_window(date)
        slots = initial_window.difference(merged_windows)
        return slots
