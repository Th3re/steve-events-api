import connexion
import logging
import pymongo
from swagger_ui_bundle import swagger_ui_3_path

from api.api.fetcher.events_fetcher import EventsFetcher
from api.date.date_proposer import DateProposer
from api.environment import Environment
from api.events.google_location import GoogleLocationFetcher
from api.gravity.center_constructor import CenterConstructor
from api.libs.db.mongo import MongoStore
from api.libs.google.google_client import GoogleClient
from api.libs.token.steve import SteveTokenService
from api.meeting.google_proposer import GooglePlaceProposer
from api.meeting.google_scheduler import GoogleScheduler
from api.meeting.point.point import MeetingPointProposerImpl

logging.basicConfig(level=logging.DEBUG)
env = Environment.read()

mongo_client = pymongo.MongoClient(env.mongo.uri, username=env.mongo.user, password=env.mongo.password)
store = MongoStore(mongo_client, env.mongo.database, env.mongo.collection)

google_client = GoogleClient(env.google.host)
meeting_scheduler = GoogleScheduler(google_client)
token_service = SteveTokenService(env.auth.url)
constructor = CenterConstructor()
location_fetcher = GoogleLocationFetcher(GoogleClient(env.google.maps_host), env.google.apikey)
fetcher = EventsFetcher(store)
proposer = DateProposer(fetcher)
place_proposer = GooglePlaceProposer(location_fetcher)
meeting_point_proposer = MeetingPointProposerImpl(fetcher, constructor, location_fetcher, place_proposer)


def main():
    options = {"swagger_path": swagger_ui_3_path}
    app = connexion.FlaskApp(
        __name__, specification_dir="openapi/", options=options
    )
    app.add_api(
        "api.yaml",
        arguments={"title": "Location API"},
        resolver=connexion.resolver.RestyResolver("api.api"),
    )
    app.run(port=env.server.port)
