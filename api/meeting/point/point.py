import logging

from typing import List
from api.date.window import Window
from api.libs.events.event import Event
from api.api.fetcher.fetcher import Fetcher
from api.meeting.proposer import PlaceProposer
from api.events.location import LocationFetcher, Place
from api.gravity.constructor import Constructor, Location
from api.meeting.point.proposer import MeetingPointProposer


LOG = logging.getLogger(__name__)


class MeetingPointProposerImpl(MeetingPointProposer):
    def __init__(self, fetcher: Fetcher, constructor: Constructor,
                 location_fetcher: LocationFetcher, place_proposer: PlaceProposer):
        self.fetcher = fetcher
        self.constructor = constructor
        self.location_fetcher = location_fetcher
        self.place_proposer = place_proposer

    def _fetch_locations(self, events: List[Event]) -> List[Location]:
        locations = [self.location_fetcher.fetch_geolocation(event.location) for event in events]
        return list(filter(lambda location: location is not None, locations))

    def propose(self, window: Window, host: str, participants: List[str]) -> List[Place]:
        attendants = participants + [host]
        events = [self.fetcher.get_previous_event(participant, window.start) for participant in attendants]
        events = list(filter(lambda event: event is not None, events))
        locations = self._fetch_locations(events)
        center = self.constructor.calculate(locations)
        return self.place_proposer.propose(center) if center else []
