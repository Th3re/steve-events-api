import abc
from datetime import datetime

from api.libs.date.formatter import DatetimeFormatter


class Window:
    START = 'start'
    END = 'end'

    date_formatter = DatetimeFormatter()

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end
    
    def to_json(self) -> dict:
        return {
            self.START: self.date_formatter.format_date(self.start),
            self.END: self.date_formatter.format_date(self.end)
        }
