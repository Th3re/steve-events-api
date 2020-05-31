from datetime import datetime
from api.date.window import Window
from api.libs.date.formatter import DATETIME_FORMAT

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


def test_merged():
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

    for tc in test_cases:
        w1 = tc['w1']
        expect = tc['expect']
        result = Window.merged(w1)
        print(f'result: {result}')
        print(f'expect: {expect}')
        assert expect == result


def test_difference():
    test_cases = [
        {
            'w': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
            'windows': [
                Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            ],
            'expect': [
                Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T10:00:00Z")),
                Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T23:59:59Z"))
            ]
        },
        {
            'w': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
            'windows': [
                Window(start=date("2020-06-05T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
            ],
            'expect': [
                Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T23:59:59Z"))
            ]
        },
        {
            'w': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
            'windows': [
                Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-07T12:00:00Z")),
            ],
            'expect': [
                Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T10:00:00Z"))
            ]
        },
        {
            'w': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
            'windows': [
                Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
                Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T14:00:00Z"))
            ],
            'expect': [
                Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T10:00:00Z")),
                Window(start=date("2020-06-06T14:00:00Z"), end=date("2020-06-06T23:59:59Z"))
            ]
        },
        {
            'w': Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T23:59:59Z")),
            'windows': [
                Window(start=date("2020-06-06T10:00:00Z"), end=date("2020-06-06T12:00:00Z")),
                Window(start=date("2020-06-06T13:00:00Z"), end=date("2020-06-06T14:00:00Z"))
            ],
            'expect': [
                Window(start=date("2020-06-06T00:00:00Z"), end=date("2020-06-06T10:00:00Z")),
                Window(start=date("2020-06-06T12:00:00Z"), end=date("2020-06-06T13:00:00Z")),
                Window(start=date("2020-06-06T14:00:00Z"), end=date("2020-06-06T23:59:59Z"))
            ]
        },
    ]

    for tc in test_cases:
        w = tc['w']
        windows = tc['windows']
        expect = tc['expect']
        result = w.difference(windows)
        print(f'result: {result}')
        print(f'expect: {expect}')
        assert expect == result
