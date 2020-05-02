import logging
from http import HTTPStatus

from api.api.api import APICode
from api.app import store

LOG = logging.getLogger(__name__)


def post(userId, get_events_request):
    LOG.info(get_events_request)
    events = store.get(userId)
    if events is None:
        return {
           "code": APICode.ERROR,
           "message": f"User {userId} events not found",
           "events": {}
        }, HTTPStatus.NOT_FOUND
    return {
       "code": APICode.OK,
       "message": f"User {userId} events",
       "events": events
    }, HTTPStatus.OK
