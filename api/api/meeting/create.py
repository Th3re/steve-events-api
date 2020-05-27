import logging
from http import HTTPStatus

from api.api.api import APICode
from api.app import meeting_scheduler, token_service
from api.meeting.scheduler import Meeting

LOG = logging.getLogger(__name__)


def create_meeting(request):
    return Meeting(
        summary=request.summary,
        start=request.start,
        end=request.end,
        location=request.location,
        participants=request.participants,
    )


def post(create_meeting_request):
    LOG.info(create_meeting_request)
    token = token_service.fetch(create_meeting_request.host)
    meeting = create_meeting(create_meeting_request)
    response = meeting_scheduler.schedule(token, meeting)
    return {
         "code": APICode.OK,
         "message": "Meeting created",
         "meeting": {"response": response}
    }, HTTPStatus.OK
