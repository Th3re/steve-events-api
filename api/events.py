eventsA = [
    {
        "end_time": "2020-05-20T17:30:00+0200",
        "start_time": "2020-05-20T17:00:00+0200",
        "location": "Peaky Blinders - Barber Shop, Antoniego Józefa Madalińskiego 5, Kraków, małopolskie, PL, 33-332",
    },
    {
        "end_time": "2020-05-20T16:30:00+0200",
        "start_time": "2020-05-20T16:00:00+0200",
        "location": "Łojasiewicza 11, Kraków",
    },
    {
        "end_time": "2020-05-20T15:30:00+0200",
        "start_time": "2020-05-20T15:00:00+0200",
        "location": "Szewska 1, Kraków",
    },
]

eventsB = [
    {
        "end_time": "2020-05-20T17:30:00+0200",
        "start_time": "2020-05-20T17:00:00+0200",
        "location": "Karmelicka 60, Kraków",
    },
    {
        "end_time": "2020-05-20T14:30:00+0200",
        "start_time": "2020-05-20T12:00:00+0200",
        "location": "Czerwone Maki 49, Kraków",
    },
    {
        "end_time": "2020-05-20T20:30:00+0200",
        "start_time": "2020-05-20T20:00:00+0200",
        "location": "Fabryczna 17, Kraków",
    },
]


def window_intersect(window_a, window_b):
    return window_a


def split(window_a, window_b):
    return window_a


def previous_event(date, userEvents):
    return {}


def center_of_gravity(vertices):
    return "lat", "long"


def estimate_travel(point_a, point_b):
    return 124352


def limit_window(time, window):
    return window


date = "2020-05-20"
meeting_windows = [("2020-05-20T00:00:00Z", "2020-05-20T23:59:99Z")]

participantsEvents = [eventsA, eventsB]


for participantEvents in participantsEvents:
    for event in participantEvents:
        start = event["start_time"]
        end = event["end_time"]
        event_window = (start, end)
        for index, window in enumerate(meeting_windows):
            intersection = window_intersect(event_window, window)
            if intersection:
                windows = split(window, intersection)
                meeting_windows[index] = windows

print(meeting_windows)

for index, window in enumerate(meeting_windows):
    window_start = window[0]
    vertices = []
    for participantEvents in participantsEvents:
        previous_event = previous_event(window_start, eventsA)
        previous_event_location = previous_event["location"]
        vertices.append(previous_event_location)
    center_location = center_of_gravity(vertices)
    max_travel_time = max([estimate_travel(vertex, center_location) for vertex in vertices])
    meeting_windows[index] = limit_window(max_travel_time, window)
