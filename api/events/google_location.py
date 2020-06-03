import logging
import urllib

from typing import Optional
from api.libs.google.client import Client
from api.gravity.constructor import Location
from api.events.location import LocationFetcher, Place


LOG = logging.getLogger(__name__)


class GoogleLocationFetcher(LocationFetcher):
    def __init__(self, client: Client, api_key: str):
        self.client = client
        self.api_key = api_key
    
    def fetch_geolocation(self, location: str) -> Optional[Location]:
        encoded_location = urllib.parse.quote_plus(location)
        response = self.client.get('maps/api/geocode/json', None, {'key': self.api_key, 'address': encoded_location})
        LOG.info(f'Fetched location: {response}')
        if response['status'] != 'OK':
            return
        place = response['results'][0]
        location = place['geometry']['location']
        return Location(location['lat'], location['lng'])

    def fetch_place(self, location: Location) -> Optional[Place]:
        params = {'key': self.api_key, 'latlng': f'{location.latitude},{location.longitude}'}
        response = self.client.get('maps/api/geocode/json', None, params)
        LOG.info(f'Fetched location: {response}')
        if response['status'] != 'OK':
            return
        place = response['results'][0]
        return Place(place['formatted_address'])
