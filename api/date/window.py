from datetime import datetime

from api.libs.date.formatter import DatetimeFormatter
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

    def difference(self, windows):
        splitted = []
        current_end = self.start
        intersections = [self.intersect(w) for w in windows]
        for window in filter(lambda x: x is not None, intersections):
            if window.start != current_end:
                splitted.append(Window(current_end, window.start))
            current_end = window.end
        if current_end != self.end:
            splitted.append(Window(current_end, self.end))
        return splitted

    @staticmethod
    def merged(windows):
        if len(windows) < 2:
            return windows
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
