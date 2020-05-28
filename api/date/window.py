from datetime import datetime

from typing import List

from api.libs.date.formatter import DatetimeFormatter, DATETIME_FORMAT
from api.libs.representation.pretty import PrettyPrint


class Window(PrettyPrint):
    START = 'start'
    END = 'end'

    date_formatter = DatetimeFormatter()

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end
    
    @staticmethod
    def initial_window(date: datetime):
        return Window(
            start=date.replace(hour=0, minute=0, second=0),
            end=date.replace(hour=23, minute=59, second=59)
        )

    def empty(self):
        return self.start.timestamp() >= self.end.timestamp()

    def split(self, window):
        intersection = self.intersect(window)
        if not intersection:
            return [self]
        w1 = Window(window.start, intersection.start)
        w2 = Window(intersection.end, window.end)
        result = []
        if not w1.empty():
            result.append(w1)
        if not w2.empty():
            result.append(w2)
        return result
    
    def intersect(self, window):
        intersection_start = max(self.start.timestamp(), window.start.timestamp())
        intersection_end = min(self.end.timestamp(), window.end.timestamp())
        if intersection_start >= intersection_end:
            return None
        return Window(
            start=datetime.fromtimestamp(intersection_start),
            end=datetime.fromtimestamp(intersection_end)
        )

    def __eq__(self, other):
        return isinstance(other, Window) \
               and self.start.timestamp() == other.start.timestamp() \
               and self.end.timestamp() == other.end.timestamp()

    def to_json(self) -> dict:
        return {
            self.START: self.date_formatter.format_date(self.start),
            self.END: self.date_formatter.format_date(self.end)
        }


date = lambda x: datetime.strptime(x, DATETIME_FORMAT)

# Intersect tests
test_cases = [
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T20:45:00Z")),
        'expect': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T20:45:00Z"))
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T19:30:00Z"), end=date("2020-06-06T20:45:00Z")),
        'expect': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T20:45:00Z"))
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:45:00Z")),
        'expect': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z"))
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:45:00Z")),
        'expect': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z"))
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T18:30:00Z"), end=date("2020-06-06T19:45:00Z")),
        'expect': None
    },
    {
        'w1': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
        'w2': Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T20:00:00Z")),
    },
]

# for tc in test_cases:
#     w1 = tc['w1']
#     w2 = tc['w2']
#     expect = tc['expect']
#     result = w1.intersect(w2)
#     assert expect == result


# split tests
split_test_cases = [
    {
        'w1': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
        'w2': Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T20:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T19:00:00Z")),
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T23:59:59Z")),
        ]
    },
    # {
    #     'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
    #     'w2': Window(start=date("2020-06-06T19:30:00Z"), end=date("2020-06-06T20:45:00Z")),
    #     'expect': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T20:45:00Z"))
    # },
    # {
    #     'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
    #     'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:45:00Z")),
    #     'expect': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z"))
    # },
    # {
    #     'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
    #     'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:45:00Z")),
    #     'expect': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z"))
    # },
    # {
    #     'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
    #     'w2': Window(start=date("2020-06-06T18:30:00Z"), end=date("2020-06-06T19:45:00Z")),
    #     'expect': None
    # },
]

for tc in split_test_cases:
    w1 = tc['w1']
    w2 = tc['w2']
    expect = tc['expect']
    result = w1.split(w2)
    print(f'result: {result}')
    print(f'expect: {expect}')
    assert expect == result

