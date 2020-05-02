import logging
from http import HTTPStatus

from api.api.api import APICode

LOG = logging.getLogger(__name__)


def post(propose_date_request):
    LOG.info(propose_date_request)
    return {
         "code": APICode.OK,
         "message": "Proposed dates",
         "dates": []
    }, HTTPStatus.OK
