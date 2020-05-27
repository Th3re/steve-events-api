import logging

from api.libs.google.client import Client
from api.meeting.scheduler import Scheduler, Meeting


LOG = logging.getLogger(__name__)


class GoogleScheduler(Scheduler):
    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    def _prepare_payload(meeting: Meeting):
        return {
            "summary": meeting.summary,
            "location": meeting.location,
            "start": {
                "dateTime": meeting.start,
                "timeZone": "Poland/Warsaw",
            },
            "end": {
                "dateTime": meeting.end,
                "timeZone": "Poland/Warsaw",
            },
            "attendees": [dict(email=participant) for participant in meeting.participants]
        }

    def schedule(self, token: str, meeting: Meeting):
        body = self._prepare_payload(meeting)
        params = dict(alt='json')
        response = self.client.post('/calendar/v3/calendars/primary/events', token, params, body)
        LOG.info(f'Meeting creation response: {response}')
