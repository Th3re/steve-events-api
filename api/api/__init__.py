import logging
from http import HTTPStatus

from api.api.api import APICode

LOG = logging.getLogger(__name__)


def post(userId):
    LOG.info(userId)
    return {
               "code": APICode.OK,
               "message": f"User {userId} events",
               "events": []
           }, HTTPStatus.OK
