import logging
from http import HTTPStatus

from api.api.api import APICode

LOG = logging.getLogger(__name__)


def post(store_events_request):
    LOG.info(store_events_request)
    return {
         "code": APICode.OK,
         "message": "Location uploaded",
         "userId": "123"
    }, HTTPStatus.OK
