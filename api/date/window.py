from datetime import datetime

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
        w1 = Window(self.start, intersection.start)
        w2 = Window(intersection.end, self.end)
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
            start=datetime.fromtimestamp(intersection_start, tz=self.start.tzinfo),
            end=datetime.fromtimestamp(intersection_end, tz=self.start.tzinfo)
        )

    def __contains__(self, window):
        return window.start.timestamp() >= self.start.timestamp() and window.end.timestamp() <= self.end.timestamp()

    def neighbor(self, window):
        return self.start == window.end or self.end == window.start

    def merge(self, window):
        if not self.intersect(window) and not self.neighbor(window):
            return sorted([self, window], key=lambda x: x.start.timestamp())
        return [Window(
            start=datetime.fromtimestamp(min(self.start.timestamp(), window.start.timestamp()), tz=self.start.tzinfo),
            end=datetime.fromtimestamp(max(self.end.timestamp(), window.end.timestamp()), tz=self.end.tzinfo)
        )]

    def split_more_xd(self, windows):
        splitted = []
        current_window = self
        for window in windows:
            result = current_window.split(window)
            splitted.append(result[0])
            current_window = result[-1]
        return splitted

    @staticmethod
    def merged(windows):
        sorted_windows = sorted(windows, key=lambda x: x.start.timestamp())
        merged_windows = []
        current_window = sorted_windows[0]
        for window in sorted_windows:
            merge_result = current_window.merge(window)
            if len(merge_result) == 1:
                current_window = merge_result[0]
            else:
                merged_windows.append(merge_result[0])
                current_window = merge_result[1]
        merged_windows.append(current_window)
        return merged_windows

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
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T19:30:00Z"), end=date("2020-06-06T20:45:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:45:00Z"), end=date("2020-06-06T22:00:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:45:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T20:30:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T21:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T21:00:00Z"), end=date("2020-06-06T22:00:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T20:30:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'expect': []
    },
]

# for tc in split_test_cases:
#     w1 = tc['w1']
#     w2 = tc['w2']
#     expect = tc['expect']
#     result = w1.split(w2)
#     print(f'result: {result}')
#     print(f'expect: {expect}')
#     assert expect == result


# test merge
test_cases = [
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T21:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T21:30:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T21:30:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T21:30:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T21:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z"))
        ]
    },
    {
        'w1': Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T12:30:00Z")),
        'expect': [
            Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T12:30:00Z")),
            Window(start=date("2020-06-06T20:30:00Z"), end=date("2020-06-06T22:00:00Z")),
        ],
    },
    {
        'w1': Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        'w2': Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T20:00:00Z")),
        'expect': [
            Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T22:00:00Z")),
        ],
    }
]
#
# for tc in test_cases:
#     w1 = tc['w1']
#     w2 = tc['w2']
#     expect = tc['expect']
#     result = w1.merge(w2)
#     print(f'result: {result}')
#     print(f'expect: {expect}')
#     assert expect == result


# test merged
test_cases = [
    {
        'w1': [
            Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T20:00:00Z")),
            Window(start=date("2020-06-06T20:00:00Z"), end=date("2020-06-06T21:00:00Z")),
            Window(start=date("2020-06-06T18:00:00Z"), end=date("2020-06-06T19:00:00Z"))
        ],
        'expect': [
            Window(start=date("2020-06-06T18:00:00Z"), end=date("2020-06-06T21:00:00Z"))
        ]
    },
    {
        'w1': [
            Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            Window(start=date("2020-06-06T11:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T21:00:00Z")),
            Window(start=date("2020-06-06T18:00:00Z"), end=date("2020-06-06T19:00:00Z"))
        ],
        'expect': [
            Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            Window(start=date("2020-06-06T18:00:00Z"), end=date("2020-06-06T21:00:00Z"))
        ]
    },
    {
        'w1': [
            Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            Window(start=date("2020-06-06T13:00:00Z"), end=date("2020-06-06T15:00:00Z")),
            Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T21:00:00Z")),
        ],
        'expect': [
            Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            Window(start=date("2020-06-06T13:00:00Z"), end=date("2020-06-06T15:00:00Z")),
            Window(start=date("2020-06-06T19:00:00Z"), end=date("2020-06-06T21:00:00Z")),
        ]
    },
]

# for tc in test_cases:
#     w1 = tc['w1']
#     expect = tc['expect']
#     result = Window.merged(w1)
#     print(f'result: {result}')
#     print(f'expect: {expect}')
#     assert expect == result
