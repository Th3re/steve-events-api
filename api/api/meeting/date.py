import logging
import datetime
from http import HTTPStatus

from api.api.api import APICode
from api.app import proposer

LOG = logging.getLogger(__name__)


def parse_date(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d')


def post(propose_date_request):
    LOG.info(propose_date_request)
    participants = propose_date_request['participants']
    date = parse_date(propose_date_request['date'])
    windows = proposer.propose(date, participants)
    dates = list(map(lambda x: x.to_json(), windows))
    return {
         "code": APICode.OK,
         "message": "Proposed dates",
         "dates": dates
    }, HTTPStatus.OK
