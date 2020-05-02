import logging
from http import HTTPStatus

from api.api.api import APICode

LOG = logging.getLogger(__name__)


def post(create_meeting_request):
    LOG.info(create_meeting_request)
    return {
         "code": APICode.OK,
         "message": "Meeting created",
         "meeting": {}
    }, HTTPStatus.OK
