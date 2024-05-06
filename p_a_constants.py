LILYPOND_VERSION = "2.24.1"

SAMPLE_RATE = 48000

# see https://en.wikipedia.org/wiki/Just_intonation

PURE_PITCHES = [
    (1, 1),
    (16, 15),
    (9, 8),
    (6, 5),
    (5, 4),
    (4, 3),
    (45, 32),
    (3, 2),
    (8, 5),
    (5, 3),
    (9, 5),
    (15, 8),
]

_PURE_PITCHES = {
    "c-flat": 9 / 8,
    "c": 6 / 5,
    "c-sharp": 5 / 4,
    "d-flat": 5 / 4,
    "d": 4 / 3,
    "d-sharp": 45 / 32,
    "e-flat": 45 / 32,
    "e": 3 / 2,
    "e-sharp": 8 / 5,
    "f-flat": 3 / 2,
    "f": 8 / 5,
    "f-sharp": 5 / 3,
    "g-flat": 5 / 3,
    "g": 9 / 5,
    "g-sharp": 15 / 8,
    "a-flat": 15 / 8,
    "a": 2,
    "a-sharp": 2 * 16 / 15,
    "b-flat": 2 * 16 / 15,
    "b": 2 * 9 / 8,
    "b-sharp": 6 / 5,
}

PURE_RATIOS = {
    'up': {
        'chromatic': ['1/1'],
        'major': ['1/1', '9/8', '5/4', '4/3', '3/2', '5/3', '15/8', ],
        'natural': ['1/1', '9/8', '6/5', '4/3', '3/2', '8/5', '9/5', ],
        'harmonic': ['1/1', '9/8', '6/5', '4/3', '3/2', '8/5', '15/8', ],
        'melodic': ['1/1', '9/8', '6/5', '4/3', '3/2', '5/3', '15/8', ]
    },
    'down': {
        'major': ['1/1', '9/8', '5/4', '4/3', '3/2', '5/3', '15/8', ],
        'natural': ['1/1', '9/8', '6/5', '4/3', '3/2', '8/5', '9/5', ],
        'harmonic': ['1/1', '9/8', '6/5', '4/3', '3/2', '8/5', '15/8', ],
        'melodic': ['1/1', '9/8', '6/5', '4/3', '3/2', '8/5', '9/5', ],
    }
}

ACCOMPANY = {
    'GP': "Grand Piano (non pure)",
    'DR': "Drone Root (incl. harmonics)",
    'DF': "Drone Fifth (incl. harmonics)",
    'PC': "Pure Chords"}
