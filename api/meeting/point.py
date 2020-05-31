from typing import List

from api.api.events.fetcher import Fetcher
from api.date.window import Window
from api.events.location import LocationFetcher
from api.gravity.constructor import Constructor, Location


class MeetingPointScheduler:
    def __init__(self, fetcher: Fetcher, constructor: Constructor, location_fetcher: LocationFetcher):
        self.fetcher = fetcher
        self.constructor = constructor
        self.location_fetcher = location_fetcher

    def _fetch_locations(self, events) -> List[Location]:
        pass

    def schedule(self, window: Window, host: str, participants: List[str]):
        host_previous_event = self.fetcher.get_previous_event(host, window.start.day)
        self.constructor.calculate()
        pass
