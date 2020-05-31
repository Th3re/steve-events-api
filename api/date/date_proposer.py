from datetime import datetime
from typing import List

from api.api.events.fetcher import ParticipantEvents, Fetcher
from api.date.proposer import Proposer
from api.date.window import Window


class DateProposer(Proposer):
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    def _participants_events(self, participants: List[str], date: datetime) -> List[ParticipantEvents]:
        return [self.fetcher.fetch_by_date(user_id, date) for user_id in participants]

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
