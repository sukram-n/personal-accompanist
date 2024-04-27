from dataclasses import dataclass

import streamlit as st

REFERENCE_PITCH = 443.0

SAMPLE_RATE = 48000

ACCOMPANY = {
    'GP': "Grand Piano (well tempered)",
    'DR': "Drone Root (incl. harmonics)",
    'DF': "Drone Fifth (incl. harmonics)",
    'PC': "Pure Chords"}

EXERCISES = ['One Octave', 'Two Octaves', 'Triads']

EVENT_VALUES = {
    '1whole notes': (1, 1),
    '2half notes': (2, 2),
    '3quarter notes': (4, 4),
    '4eigth notes': (8, 8),
    '5eigth triplets': (12, 8),
    '6sixteenth': (16, 16)}

TRANSLATIONS = {
    "0": "\\Nf",
    "1": "\\If",
    "2": "\\Mf",
    "3": "\\Rf",
    "4": "\\Pf",
    "t": "\\Tf",
    "-": "",
    "B": '\\clef "bass_8"\n',
    "T": '\\clef "tenor_8"\n',
    "V": '\\clef "violin_8"\n',
    "G": '_\\Gstring\n',
    "D": '_\\Dstring\n',
    "A": '_\\Astring\n',
    "E": '_\\Estring\n',
}

HEAD = f"""\\version "2.24.1"
\\language "deutsch"
\\include "../commons.ly"

"""

reference_pitch = 443.0  # a'

MAJOR_PURE_RATIOS = [1/1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8,
                     2/1,
                     15/8, 5/3, 3/2, 4/3, 5/4, 9/8,
                     1/1]

MAJOR_ONE_OCTAVE_PURE_CHORDS = [
    [1/1, 3/4, 5/8],
    [9/8, 15/16, 3/4],
    [5/4, 1/1, 3/4],
    [4/3, 1/1, 5/6],
    [3/2, 5/4, 1/1],
    [5/3, 4/3, 1/1],
    [15/8, 3/2, 9/8],
    [2/1, 3/2, 5/4],
    [15/8, 3/2, 9/8],
    [5/3, 4/3, 1/1],
    [3/2, 5/4, 1/1],
    [4/3, 1/1, 5/6],
    [5/4, 1/1, 3/4],
    [9/8, 15/16, 3/4],
    [1/1, 3/4, 5/8],
]

MAJOR_TWO_OCTAVES_PURE_CHORDS = [
    [1/1, 3/4, 5/8],
    [9/8, 15/16, 3/4],
    [5/4, 1/1, 3/4],
    [4/3, 1/1, 5/6],
    [3/2, 5/4, 1/1],
    [5/3, 4/3, 1/1],
    [15/8, 3/2, 9/8],
    [2/1, 3/2, 5/4],

    [9 / 4, 15 / 8, 3 / 2],
    [5 / 2, 2 / 1, 3 / 2],
    [8 / 3, 2 / 1, 5 / 3],
    [3 / 1, 5 / 2, 2 / 1],
    [10 / 3, 8 / 3, 2 / 1],
    [15 / 4, 3 / 1, 9 / 4],

    [4 / 1, 3 / 1, 5 / 2],

    [15/4, 3/1, 9/4],
    [10/3, 8/3, 2/1],
    [3/1, 5/2, 2/1],
    [8/3, 2/1, 5/3],
    [5/2, 2/1, 3/2],
    [9/4, 15/8, 3/2],

    [2/1, 3/2, 5/4],

    [15/8, 3/2, 9/8],
    [5/3, 4/3, 1/1],
    [3/2, 5/4, 1/1],
    [4/3, 1/1, 5/6],
    [5/4, 1/1, 3/4],
    [9/8, 15/16, 3/4],
    [1/1, 3/4, 5/8],
]
PURE_CHORDS = {'One Octave': MAJOR_ONE_OCTAVE_PURE_CHORDS, 'Two Octaves': MAJOR_TWO_OCTAVES_PURE_CHORDS}
NATMI_PURE_RATIOS = [1/1, 9/8, 6/5, 4/3, 3/2, 8/5, 9/5,
                     2/1,
                     9/5, 8/5, 3/2, 4/3, 6/5, 9/8,
                     1/1]
HARMI_PURE_RATIOS = [1/1, 9/8, 6/5, 4/3, 3/2, 8/5, 15/8,
                     2/1,
                     15/8, 8/5, 3/2, 4/3, 6/5, 9/8,
                     1/1]
MELMI_PURE_RATIOS = [1/1, 9/8, 6/5, 4/3, 3/2, 5/3, 15/8,
                     2/1,
                     9/5, 8/5, 3/2, 4/3, 6/5, 9/8,
                     1/1]

if "reference_pitch" in st.session_state:
    reference_pitch = st.session_state.reference_pitch
else:
    reference_pitch = REFERENCE_PITCH

#                              v
# c     g    d    a   e   h   fis cis gis dis ais eis his
# deses ases eses bes fes ces ges des as  es  b   f   c
#                              ^


def set_pitches(r_p):
    pitches = {
        "h,,,": r_p/16 * 9/8,
        "ces,,": r_p/16 * 9/8,
        "c,,": r_p/16 * 6/5,
        "cis,,": r_p/16 * 5/4,
        "des,,": r_p/16 * 5/4,
        "d,,": r_p/16 * 4/3,
        "dis,,": r_p/16 * 45/32,
        "es,,": r_p/16 * 45/32,
        "e,,": r_p/16 * 3/2,
        "eis,,": r_p/16 * 3/2,
        "f,,": r_p/16 * 8/5,
        "fis,,": r_p/16 * 5/3,
        "ges,,": r_p/16 * 5/3,
        "g,,": r_p/16 * 3/2,
        "gis,,": r_p/16 * 15/8,
        "as,,": r_p / 16 * 15 / 8,

        "a,,": r_p/8,
        "b,,": r_p/8 * 16/15,
        "h,,": r_p/8 * 9/8,
        "ces,": r_p/8 * 9/8,
        "c,": r_p/8 * 6/5,
        "cis,": r_p/8 * 5/4,
        "des,": r_p/8 * 5/4,
        "d,": r_p/8 * 4/3,
        "dis,": r_p/8 * 45/32,
        "es,": r_p/8 * 45/32,
        "e,": r_p/8 * 3/2,
        "eis,": r_p/8 * 8/5,
        "f,": r_p/8 * 8/5,
        "ges,": r_p/8 * 5/3,
        "fis,": r_p/8 * 5/3,
        "g,": r_p/8 * 9/5,
        "gis,": r_p/8 * 15/8,
        "as,": r_p / 8 * 15 / 8,

        "a,": r_p/4,
        "b,": r_p/4 * 16/15,
        "h,": r_p/4 * 9/8,
        "ces": r_p/4 * 9/8,
        "c": r_p/4 * 6/5,
        "cis": r_p/4 * 5/4,
        "des": r_p/4 * 5/4,
        "d": r_p/4 * 4/3,
        "dis": r_p/4 * 45/32,
        "es": r_p/4 * 45/32,
        "e": r_p/4 * 3/2,
        "f": r_p/4 * 8/5,
        "fis": r_p/4 * 5/3,
        "ges": r_p/4 * 5/3,
        "g": r_p/4 * 9/5,
        "gis": r_p/4 * 15/8,
        "as": r_p / 4 * 15 / 8,

        "a": r_p/2,
        "b": r_p/2 * 16/15,
        "h": r_p/2 * 9/8,
        "ces'": r_p/2 * 9/8,
        "c'": r_p/2 * 6/5,
        "cis'": r_p/2 * 5/4,
        "des'": r_p/2 * 5/4,
        "d'": r_p/2 * 4/3,
        "dis'": r_p/2 * 45/32,
        "es'": r_p/2 * 45/32,
        "e'": r_p/2 * 3/2,
        "f'": r_p/2 * 8/5,
        "fis'": r_p/2 * 5/3,
        "ges'": r_p/2 * 5/3,
        "g'": r_p/2 * 9/5,
        "gis'": r_p/2 * 15/8,
        "as'": r_p / 2 * 15 / 8,

        "a'": r_p,
        "b'": r_p * 16/15,
        "h'": r_p * 9/8,
        "ces''": r_p * 9/8,
        "c''": r_p * 6/5,
        "cis''": r_p * 5/4,
        "des''": r_p * 5/4,
        "d''": r_p * 4/3,
        "dis''": r_p * 45/32,
        "es''": r_p * 45/32,
        "e''": r_p * 3/2,
        "f''": r_p * 8/5,
        "fis''": r_p * 5/3,
        "ges''": r_p * 5/3,
        "g''": r_p * 9/5,
        "gis''": r_p * 15/8,
        "as''": r_p * 15 / 8,

        "a''": r_p * 2,
        "b''": r_p * 2 * 16/15,
        "h''": r_p * 2 * 9/8,
        "ces'''": r_p * 2 * 9/8,
        "c'''": r_p * 2 * 6/5,
        "des'''": r_p * 2 * 5/4,
        "cis'''": r_p * 2 * 5/4,
        "d'''": r_p * 2 * 4/3,
        "dis'''": r_p * 2 * 45/32,
        "es'''": r_p * 2 * 45/32,
        "e'''": r_p * 2 * 3/2,
        "f'''": r_p * 2 * 8/5,
        "fis'''": r_p * 2 * 5/3,
        "ges'''": r_p * 2 * 5/3,
        "g'''": r_p * 2 * 9/5,
        "gis'''": r_p * 2 * 15/8,
        "as'''": r_p * 2 * 15 / 8,

        "a'''": r_p * 4,
        "b'''": r_p * 4 * 16/15
    }
    return pitches


SCALES = {
    'C': {
        "One Octave": {
            "pitches": "c, d, e, f, g, a, h, c h, a, g, f, e, d, c, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "c, d, e, f, g, a, h, c d e f g a h c' h a g f e d c h, a, g, f, e, d, c, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            'pitches': "c, e, g, e, c, R c, e, g, c g, e, c, R c, e, g, c e c g, e, c, R c, e, g, c e g e c g, e, "
                       "c, R c, e, g, c e g c' g e c g, e, c, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'a': {
        "One Octave": {
            "pitches": "a,, h,, c, d, e, fis, gis, a, g, f, e, d, c, h,, a,, R",
            'fingers': "0 1 - - - -   2   - - 2 - - - - -",
            'clefs': "B - - - - -   -   - - - - - - - -",
            'strings': "A - - - - -   D   - - - - - - - -"
        },
        "Two Octaves": {
            "pitches": "a,, h,, c, d, e, fis, gis, a, h, c d e fis gis a g f e d c h, a, g, f, e, d, c, h,, a,, R",
            'fingers': "0 1 - - - -   1   1 - 1 - 1 -   2   - 10 4 - 4 - 4 - 0 2 - - - - -",
            'clefs': "B - - - - -   -   - - - T - -   -   - -  - - - - B - - - - - - - -",
            'strings': "A - - D - -   G   - - - - - -   -   - -  - - - - - - - - - - - - -"
        },
        "Triads": {
            'pitches': "a,, c, e, c, a,, R a,, c, e, a, e, c, a,, R a,, c, e, a, c a, e, c, a,, R a,, c, e, a, "
                       "c e c a, e, c, a, R a,, c, e, a,  c e a e c a, e, c, a,, R",
            'fingers': "0 2 - - - - 0 2 - - - - - - 0 2 - 1 4 1 - - - - 0 2 - - 4 - - 1 - - 0 - 0 2 1 10 t 2 3 - - 10 "
                       "1 - ",
            'clefs': "B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -  - -",
            'strings': "A - - - - - - - - G - - - - - - D - - - D - - - A E - D - - - - - E - - A E - A  - D - - - A  D"
        },
    },
    'G': {
        "One Octave": {
            "pitches": "g,, a,, h,, c, d, e, fis, g, fis, e, d, c, h,, a,, g,, R",
            'fingers': "2 - - - - - 2   - 4   - - - - - -",
            'clefs': "B -",
            'strings': "E -"
        },
        "Two Octaves": {
            "pitches": "g,, a,, h,, c, d, e, fis, g, a, h, c d e fis g fis e d c h, a, g, fis, e, d, c, h,, a,, g,, R",
            'fingers': "2 - - - - - -   1 - 1 - 1 - 2   30 -   4 - 2 - 4 - 4   - - - - - -",
            'clefs': "B - - - - - -   - - - - - T -   -  -   - B",
            'strings': "E - - - - - - - - - G - - - -   -  -   - - - - D - -   - - - - - -"
        },
        "Triads": {
            'pitches': "g,, h,, d, h,, g,, R g,, h,, d, g, d, h,, g,, R g,, h,, d, g, h, g, d, h,, g,, R g,, h,, d, "
                       "g, h, d h, g, d, h,, g,, R g,, h,, d, g, h, d g d h, g, d, h,, g,,",
            'fingers': "2 - 0 - - - 2 - 0 - - - - - 2 - 0 - 4 - - - - - 2 - - 0 1 4 - 0 - 1 - - 2 - - - 4 - 30 1 - 0 "
                       "- - -",
            'strings': "E - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - D G -  G - - "
                       "- - -",
            'clefs': "B"
        },
    },
    'e': {
        "One Octave": {
            "pitches": "e,, fis,, g,, a,, h,, cis, dis, e, d, c, h,, a,, g,, fis,, e,, R",
            "fingers": "0 - ",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "e,, fis,, g,, a,, h,, cis, dis, "
                       "e, fis, g, a, h, cis dis "
                       "e d c h, a, g, fis, "
                       "e, d, c, h,, a,, g,, fis,, e,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "e,, g,, h,, g,, e,, R e,, g,, h,, e, h,, g,, e,, R e,, g,, h,, e, g, e, h,, g,, e,, R e,, g,, "
                       "h,, e, g, h, g, e, h,, g,, e,, R e,, g,, h,, e, g, h, e h, g, e, h,, g,, e,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'D': {
        "One Octave": {
            "pitches": "d, e, fis, g, a, h, cis d cis h, a, g, fis, e, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "d, e, fis, g, a, h, cis d e fis g a h cis' d' cis' h a g fis e d cis h, a, g, fis, e, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "d, fis, a, fis, d, R d, fis, a, d a, fis, d, R d, fis, a, d fis d  a, fis, d, R d, fis, a, "
                       "d fis a fis d  a, fis, d, R d, fis, a, d fis a d' a fis d  a, fis, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'h': {
        "One Octave": {
            "pitches": "h,, cis, d, e, fis, gis, ais, h, a, g, fis, e, d, cis, h,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "h,, cis, d, e, fis, gis, ais, h, cis d e fis gis ais h a g fis e d cis h, a, g, fis, e, d, "
                       "cis, h,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "h,, d, fis, d, h,, R h,, d, fis, h, fis, d, h,, R h,, d, fis, h, d h, fis, d, h,, R h,, d, "
                       "fis, h, d fis d h, fis, d, h,, R h,, d, fis, h, d fis h fis d h, fis, d, h,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'A': {
        "One Octave": {
            'pitches': "a,, h,, cis, d, e, fis, gis, a, gis, fis, e, d, cis, h,, a,, R",
            'fingers': "0 1 -   - - -   2   - -   4   - - -   - -",
            'clefs': "B - -   - - -   -   - -   -   - - -   - -",
            'strings': "A - -   - - -   D   - -   -   - - -   - -"
        },
        "Two Octaves": {
            'pitches': "a,, h,, cis, d, e, fis, gis, a, h, cis d e fis gis a gis fis e d cis h, a, gis, fis, e, d, R"
                       "cis, h,, a,,",
            'fingers': "0 1 -   - - -   1   1 - 2   - 1 -   2   - -   4   - 4 -   4 - 1   4   - - -   - -",
            'clefs': "B - -   - - -   -   - - -   T - -   -   - -   -   - - -   - B -   -   - - -   - -",
            'strings': "A - -   - - -   -   - - -   - - -   -   - -   -   - - -   - - -   -   - - -   - -"
        },
        "Triads": {
            'pitches': "a,, cis, e, cis, a,, R a,, cis, e, a, e, cis, a,, R a,, cis, e, a, cis a, e, cis, a,, R "
                       "a,, cis, e, a, cis e cis a, e, cis, a,, R a,, cis, e, a,  cis e a e cis a, e, cis, a,, R",
            'fingers': "0 4   - -   - - 0 4   - - - -   - - 0 4   - 4 -   - 1 -   - - 0 4   - 2 -   4 -   - 1 -   - - "
                       "0 4   - 10 t   2 3 - -   10 1 -   - -",
            'clefs': "B -   - -   - - - -   - - - -   - - - -   - - -   - - -   - - - -   - - -   - -   - - -   - - - "
                     "-   - -  -   - - - -   -  - -   - -",
            'strings': "A -   - -   - - - -   - G - -   - - - -   D - -   - D -   - - A -   - D -   - -   - D -   - - "
                       "A E - A  D   - - - -   A  D -   - -"
        },
    },
    'fis': {
        "One Octave": {
            "pitches": "fis,, gis,, a,, h,, cis, dis, eis, fis, e, d, cis, h,, a,, gis,, fis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "fis,, gis,, a,, h,, cis, dis, eis, fis, gis, a, h, cis dis eis fis e d cis h, a, gis, fis, e, "
                       "d, cis, h,, a,, gis,, fis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "fis,, a,, cis, a,, fis,, R fis,, a,, cis, fis, cis, a,, fis,, R fis,, a,, cis, fis, a, fis, "
                       "cis, a,, fis,, R fis,, a,, cis, fis, a, cis a, fis, cis, a,, fis,, R fis,, a,, cis, fis, a, "
                       "cis fis cis a, fis, cis, a,, fis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'E': {
        "One Octave": {
            "pitches": "e,, fis,, gis,, a,, h,, cis, dis, e, dis, cis, h,, a,, gis,, fis,, e,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "e,, fis,, gis,, a,, h,, cis, dis, "
                       "e, fis, gis, a, h, cis dis "
                       "e dis cis h, a, gis, fis, "
                       "e, dis, cis, h,, a,, gis,, fis,, e,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "e,, gis,, h,, gis,, e,, R e,, gis,, h,, e, h,, gis,, e,, R e,, gis,, h,, e, gis, e, h,, gis,, "
                       "e,, R e,, gis,, h,, e, gis, h, gis, e, h,, gis,, e,, R e,, gis,, h,, e, gis, h, e h, gis, e, "
                       "h,, gis,, e,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'cis': {
        "One Octave": {
            "pitches": "cis, dis, e, fis, gis, ais, his, cis h, a, gis, fis, e, dis, cis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "cis, dis, e, fis, gis, ais, his, cis  dis e fis gis ais his cis' h a gis fis e dis cis  h, a, "
                       "gis, fis, e, dis, cis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "cis, e, gis, e, cis, R cis, e, gis, cis gis, e, cis, R cis, e, gis, cis e cis gis, e, cis, "
                       "R cis, e, gis, cis e gis e cis gis, e, cis, R cis, e, gis, cis e gis cis' gis e cis gis, e, "
                       "cis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'H': {
        "One Octave": {
            "pitches": "h,, cis, dis, e, fis, gis, ais, h, ais, gis, fis, e, dis, cis, h,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "h,, cis, dis, e, fis, gis, ais, h, cis dis e fis gis ais h ais gis fis e dis cis h, ais, "
                       "gis, fis, e, dis, cis, h,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "h,, dis, fis, dis, h,, R h,, dis, fis, h, fis, dis, h,, R h,, dis, fis, h, dis h, fis, dis, "
                       "h,, R h,, dis, fis, h, dis fis dis h, fis, dis, h,, R h,, dis, fis, h, dis fis h fis dis h, "
                       "fis, dis, h,, R ",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'gis': {
        "One Octave": {
            "pitches": "gis,, ais,, h,, cis, dis, eis, fisis, gis, fis, e, dis, cis, h,,  ais,, gis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "gis,, ais,, h,, cis, dis, eis, fisis, gis, ais, h, cis dis eis fisis gis fis e "
                       "dis cis h, ais, gis, fis, e, dis, cis, h,, ais,, gis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "gis,, h,, dis, h,, gis,, R gis,, h,, dis, gis, dis, h,, gis,, R gis,, h,, dis, gis, h, gis, "
                       "dis, h,, gis,, R gis,, h,, dis, gis, h, dis h, gis, dis, h,, gis,, R gis,, h,, dis, gis, h, "
                       "dis gis dis h, gis, dis, h,, gis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'Fis': {
        "One Octave": {
            "pitches": "fis,, gis,, ais,, h,, cis, dis, eis, fis, eis, dis, cis, h,, ais,, gis,, fis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "fis,, gis,, ais,, h,, cis, dis, eis, fis, gis, ais, h, cis dis eis fis eis dis cis h, ais, "
                       "gis, fis, eis, dis, cis, h,, ais,, gis,, fis,,R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "fis,, ais,, cis,  ais,, fis,, R fis,, ais,, cis, fis, cis, ais,, fis,, R fis,, ais,, cis, "
                       "fis, ais, fis, cis, ais,, fis,, R fis,, ais,, cis, fis, ais, cis ais, fis, cis, ais,, fis,, "
                       "R fis,, ais,, cis, fis, ais, cis fis cis ais, fis, cis, ais,, fis,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'dis': {
        "One Octave": {
            "pitches": "dis, eis, fis, gis, ais, his, cisis dis cis h, ais, gis, fis, eis, dis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "dis, eis, fis, gis, ais, his, cisis dis eis  fis gis ais his cisis' dis' cis' h ais gis "
                       "fis eis dis cis h, ais, gis, fis, eis, dis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "dis, fis, ais, fis, dis, R dis, fis, ais, dis ais, fis, dis, R dis, fis, ais, dis fis dis "
                       "ais, fis, dis, R dis, fis, ais, dis fis ais fis dis ais, fis, dis, R dis, fis, ais, "
                       "dis fis ais dis' ais fis dis ais, fis, dis, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'Ges': {
        "One Octave": {
            "pitches": "ges,, as,, b,, ces, des, es, f, ges, f, es, des, ces, b,, as,, ges,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "ges,, as,, b,, ces, des, es, f, ges, as, b, ces des es f ges f es des ces b, as, ges, f, es, "
                       "des, ces, b,, as,, ges,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "ges,, b,, des, b,, ges,, R ges,, b,, des, ges, des, b,, ges,, R ges,, b,, des, ges, b, ges, "
                       "des, b,, ges,, R ges,, b,, des, ges, b, des b, ges, des, b,, ges,, R ges,, b,, des, ges, b, "
                       "des ges des b, ges, des, b,, ges,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'es': {
        "One Octave": {
            "pitches": "es, f, ges, as, b, c d es des ces b, as, ges, f, es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "es, f, ges, as, b, c d es f ges as b c' d' es' des' ces' b as ges f es des ces b, as, ges, f, "
                       "es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "es, ges, b, ges, es, R es, ges, b, es b, ges, es, R es, ges, b, es ges es b, ges, es, R es, "
                       "ges, b, es ges b ges es b, ges, es, R es, ges, b, es ges b es' b ges es b, ges, es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'Des': {
        "One Octave": {
            "pitches": "des, es, f, ges, as, b, c des c b, as, ges, f, es, des, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "des, es, f, ges, as, b, c des es f ges as b c' des' c' b as ges f es des c b, as, ges, f, es, "
                       "des, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "des, f, as, f, des, R des, f, as, des as, f, des, R des, f, as, des f des as, f, des, R des, "
                       "f, as, des f as f des as, f, des, R des, f, as, des f as des' as f des as, f, des, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'b': {
        "One Octave": {
            "pitches": "b,, c, des, es, f, g, a, b, as, ges, f, es, des, c, b,, R",
            "fingers": "1 2 - 1 - 0 - - - 4 - 4 - 4 - -",
            "clefs":   "",
            "strings": "- - - - - - - - - - - A",
        },
        "Two Octaves": {
            "pitches": "b,, c, des, es, f, g, a, b, c des es f g a b as ges f es des c b, as, ges, f, es, des, c, b,, R",
            "fingers": "1 2 - 1 - 0 - - 2 - 1 - t 1 - 1 4 - 4 - 4 -  4 - 4 - 4 - 1",
            "clefs":   "- - - - - - - - - - T - - - - - - - - - - - B -",
            "strings": "- - - - - - - - - - - - - - - - - - - - - - D -",
        },
        "Triads": {
            "pitches": "b,, des, f, des, b,, R b,, des, f, b, f, des, b,, R b,, des, f, b, des b, f, des, b,, R b,, "
                       "des, f, b, des f des b, f, des, b,, R b,, des, f, b, des f b f des b, f, des, b,, R",
            "fingers": "1 4 - - - - 1 4 - - - - 1 - 1 2 - 1 4 1 - - 1 - 4 - 1 - 4 - - 1 - 1 - - 1 4 - - t 2 3 - - 2 - "
                       "- 1 -",
            "clefs":   " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - T - - B -",
            "strings": "A - - - - - - - - - - - - - A - - - - - - - - - A D A - - - - - - - - - E - A - - - ",
        },
    },
    'As': {
        "One Octave": {
            "pitches": "as,, b,, c, des, es, f, g, as, g, f, es, des, c, b,, as,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "as,, b,, c, des, es, f, g, as, b, c des es f g as g f es des c b, as, g, f, es, des, c, b,, "
                       "as,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "as,, c, es, c, as,, R as,, c, es, as, es, c, as,, R as,, c, es, as, c as, es, c, as,, R as,, "
                       "c, es, as, c es c as, es, c, as,, R as,, c, es, as, c es as es c as, es, c, as,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'f': {
        "One Octave": {
            "pitches": "f,, g,, as,, b,, c, d, e, f, es, des, c, b,, as,, g,, f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "f,, g,, as,, b,, c, d, e, f, g, as, b, c d e f es des c b, as, g, f, es, des, c, b,, as,, g,, "
                       "f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "f,, as,, c, as,, f,, R f,, as,, c, f, c, as,, f,, R f,, as,, c, f, as, f, c, as,, f,, R f,, "
                       "as,, c, f, as, c as, f, c, as,, f,, R f,, as,, c, f, as, c f c as, f, c, as,, f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'Es': {
        "One Octave": {
            "pitches": "es, f, g, as, b, c d es d c b, as, g, f, es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "es, f, g, as, b, c d es f g as b c' d' es' d' c' b as g f es d c b, as, g, f, es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "es, g, b, g, es, R es, g, b, es b, g, es, R es, g, b, es g es b, g, es, R es, g, b, es g b g "
                       "es b, g, es, R es, g, b, es g b es' b g es b, g, es, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'c': {
        "One Octave": {
            "pitches": "c, d, es, f, g, a, h, c b, as, g, f, es, d, c, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "c, d, es, f, g, a, h, c d es f g a h c' b as g f es d c b, as, g, f, "
                       "es, d, c, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "c, es, g, es, c, R c, es, g, c g, es, c, R c, es, g, c es c g, es, c, "
                       "R c, es, g, c es g es c g, es, c, R c, es, g, c es g c' g es c g, es, c"
                       ", R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'B': {
        "One Octave": {
            'pitches': "b,, c, d, es, f, g, a, b, a, g, f, es, d, c, b,,",
            'fingers': "1 - - -  - - - - - - - -  - - -",
            'clefs': "B - - -  - - - - - - - -  - - -",
            'strings': "A - - -  - - - - - - - -  - - -"
        },
        "Two Octaves": {
            'pitches': "b,, c, d, es, f, g, a, b, c d es f g a b a g f es d c b, a, g, f, es, d, c, b,,",
            'fingers': "1 - - -  - - - - 1 - 1  - t - - - - 4 -  4 - 4 - - - -  - - -",
            'clefs': "B - - -  - - - - T - -  - - - - - - - -  - - B - - - -  - - -",
            'strings': "A - - -  - - - - - - - -  - - - - - - -  - - - - - - -  - - -"
        },
        "Triads": {
            'pitches': "b,, d, f, d, b,, R b,, d, f, b, f, d, b,, R b,, d, f, b, d b, f, d, b,, R b,, d, f, b, "
                       "d f d b, f, d, b,, R b,, d, f, b, d f b f d b, f, d, b,, R",
            'fingers': "1 - - - - - 1 - - - - - - - 1 0 4 - - - - 0 - - 1 0 2 - - 4 1 - - 0 - - 2 - 4 - t 2 3 - - 4 - "
                       "1 - -",
            'clefs': "B -",
            'strings': "A - - - - - A - - - - - - - - - A - - D A - - - - - A D - - - - - - - - E - - - - - - - - - - "
                       "- - E"
        },
    },
    'g': {
        "One Octave": {
            'pitches': "g,, a,, b,, c, d, e, fis, g, f, es, d, c, b,, a,, g,,",
            'fingers': "4 - - - - - -   - 4 -  - - - - -",
            'clefs': "B - - - - - -   - - -  - - - - -",
            'strings': "E - - - - - -   - - -  - - - - -"
        },
        "Two Octaves": {
            'pitches': "g,, a,, b,, c, d, e, fis, g, a, b, c d e fis g f es d c b, a, g, f, es, d, c, b,, a,, g,,",
            'fingers': "4 - - - 0 1 -   0 - 1 - 1 - 2   40 4 -  4 - 4 - - - -  - - - - -",
            'clefs': "B - - - - - -   - - - - - T -   -  - -  - - - B - - -  - - - - -",
            'strings': "E - - - - - -   - - - - - - -   -  - -  - - - - - - -  - - - - -"
        },
        "Triads": {
            'pitches': "g,, b,, d, b,, g,, R g,, b,, d, g, d, b,, g,, R g,, b,, d, g, b, g, d, b,, g,, R g,, b,, d, "
                       "g, b, d b, g, d, b,, g,, R g,, b,, d, g, b, d g  d b, g, d, b,, g,, R",
            'fingers': "4 - - - - - 4 - - 0 - - - - 4 - - - - - - - - - 4 - - - 4 - - 0 - 1 - - 4 - - 0 2 - 30 1 - 0 "
                       "- 1",
            'clefs': "B - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - "
                     "- -",
            'strings': "E - - - - - - - - - - - - - - - - - - - - - - - - - - - D - - - - - - - - - - - D - -  - - - "
                       "- -"
        },
    },
    'F': {
        "One Octave": {
            "pitches": "f,, g,, a,, b,, c, d, e, f, e, d, c, b,, a,, g,, f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "f,, g,, a,, b,, c, d, e, f, g, a, b, c d e f e d c b, a, g, f, e, d, c, b,, a,, g,, f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "f,, a,, c, a,, f,, R f,, a,, c, f, c, a,, f,, R f,, a,, c, f, a, f, c, a,, f,, R f,, a,, c, "
                       "f, a, c a, f, c, a,, f,, R f,, a,, c, f, a, c f c a, f, c, a,, f,, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    },
    'd': {
        "One Octave": {
            "pitches": "d, e, f, g, a, h, cis d c b, a, g, f, e, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Two Octaves": {
            "pitches": "d, e, f, g, a, h, cis d e f g a h cis' d' c' b a g f e d c b, a, g, f, e, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
        "Triads": {
            "pitches": "d, f, a, f, d, R d, f, a, d a, f, d, R d, f, a, d f d a, f, d, R d, f, a, d f a f d a, f, d, "
                       "R d, f, a, d f a d' a f d a, f, d, R",
            "fingers": "",
            "clefs":   "",
            "strings": "",
        },
    }
}
