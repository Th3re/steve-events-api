import logging

from api.libs.environment.environmentreader import EnvironmentReader
from api.libs.representation.pretty import PrettyPrint

LOG = logging.getLogger(__name__)


class Server(EnvironmentReader):
    def __init__(self):
        super()
        self.port = self.get('port')


class Environment(PrettyPrint):
    def __init__(self):
        self.server = Server()

    @staticmethod
    def read():
        env = Environment()
        LOG.info(f'Environment: {env}')
        return env
