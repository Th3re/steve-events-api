from typing import List

from api.events.location import LocationFetcher
from api.gravity.constructor import Location
from api.meeting.proposer import PlaceProposer


class GooglePlaceProposer(PlaceProposer):
    def __init__(self, location_fetcher: LocationFetcher):
        self.location_fetcher = location_fetcher

    def propose(self, location: Location) -> List[str]:
        place = self.location_fetcher.fetch_place(location)
        return [place.address] if place else []
