import logging

from api.libs.environment.environmentreader import EnvironmentReader
from api.libs.representation.pretty import PrettyPrint
from api.libs.db.mongo import Mongo

LOG = logging.getLogger(__name__)


class Server(EnvironmentReader):
    def __init__(self):
        super()
        self.port = self.get('port')


class Google(EnvironmentReader):
    def __init__(self):
        super()
        self.host = self.get('host')
        self.maps_host = self.get('maps_host')
        self.apikey = self.get('apikey')


class Auth(EnvironmentReader):
    def __init__(self):
        super()
        self.url = self.get('url')


class Environment(PrettyPrint):
    def __init__(self):
        self.server = Server()
        self.mongo = Mongo()
        self.google = Google()
        self.auth = Auth()

    @staticmethod
    def read():
        env = Environment()
        LOG.info(f'Environment: {env}')
        return env
