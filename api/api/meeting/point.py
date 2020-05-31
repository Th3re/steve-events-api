import logging
from http import HTTPStatus

from api.api.api import APICode

LOG = logging.getLogger(__name__)


def post(propose_meeting_point_request):
    LOG.info(propose_meeting_point_request)
    return {
         "code": APICode.OK,
         "message": "Proposed meeting points",
         "locations": []
    }, HTTPStatus.OK
