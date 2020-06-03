import logging
from http import HTTPStatus

from api.api.api import APICode
from api.app import meeting_point_proposer
from api.date.window import Window
from api.libs.date.formatter import DatetimeFormatter

LOG = logging.getLogger(__name__)


def post(propose_meeting_point_request):
    LOG.info(propose_meeting_point_request)
    start = propose_meeting_point_request['start']
    end = propose_meeting_point_request['end']
    participants = propose_meeting_point_request['participants']
    host = propose_meeting_point_request['host']
    formatter = DatetimeFormatter()
    window = Window(formatter.parse_date(start), formatter.parse_date(end))
    meeting_points = meeting_point_proposer.propose(window, host, participants)
    return {
         "code": APICode.OK,
         "message": "Proposed meeting points",
         "meetingPoints": meeting_points
    }, HTTPStatus.OK
