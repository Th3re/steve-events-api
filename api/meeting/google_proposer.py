from typing import List

from api.gravity.constructor import Location
from api.meeting.proposer import PlaceProposer
from api.events.location import LocationFetcher, Place


class GooglePlaceProposer(PlaceProposer):
    def __init__(self, location_fetcher: LocationFetcher):
        self.location_fetcher = location_fetcher

    def propose(self, location: Location) -> List[Place]:
        place = self.location_fetcher.fetch_place(location)
        return [place] if place else []
