import logging

from typing import Optional
from datetime import datetime
from api.libs.events.event import Event
from api.api.fetcher.fetcher import Fetcher, ParticipantEvents

LOG = logging.getLogger(__name__)


class EventsFetcher(Fetcher):
    def __init__(self, store):
        self.store = store
    
    def fetch(self, user_id: str):
        events = [event for event in [Event.from_json(e) for e in self.store.get(user_id)]]
        return ParticipantEvents(user_id, events)

    def fetch_by_date(self, user_id: str, date: datetime):
        events = [event for event in [Event.from_json(e) for e in self.store.get(user_id)]
                  if event.start_time.day == date.day or event.end_time.day == date.day]
        return ParticipantEvents(user_id, events)

    def get_previous_event(self, user_id: str, date: datetime) -> Optional[Event]:
        user_events = self.fetch_by_date(user_id, date).events
        past_events = filter(lambda x: x.end_time.timestamp() < date.timestamp(), user_events)
        events = sorted(past_events, key=lambda x: x.end_time.timestamp())
        return events[-1] if events else None
