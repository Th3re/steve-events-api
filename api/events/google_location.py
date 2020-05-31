from typing import Optional

from api.events.location import LocationFetcher
from api.gravity.constructor import Location
from api.libs.google.client import Client


class GoogleLocationFetcher(LocationFetcher):
    def __init__(self, client: Client):
        self.client = client
    
    def fetch(self, location: str) -> Optional[Location]:
        pass