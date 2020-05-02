import logging
from http import HTTPStatus

from api.api.api import APICode
from api.app import store

LOG = logging.getLogger(__name__)


def post(store_events_request):
    LOG.info(store_events_request)
    identifier = store_events_request['userId']
    data = store_events_request['events']
    store.save(identifier, data)
    return {
         "code": APICode.OK,
         "message": "Events stored",
         "userId": identifier
    }, HTTPStatus.OK
