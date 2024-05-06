import uuid

from p_a_practice import Practices
from p_a_lilypond import Lilypond
from p_a_audio import Audio
from p_a_gui import GUI

import p_a_constants as cst


class PersonalAccompanist:

    def __init__(self):

        self.basename = uuid.uuid4().hex

        self.pitches = None
        self._total_duration = 0
        self.practice = Practices()
        self.lilypond = Lilypond(self.basename, self.practice)
        self.audio = Audio(self.basename, self.practice)
        self.set_pitches()

        self.gui = GUI(self.basename, practice=self.practice, lilypond=self.lilypond, audio=self.audio)

    def set_pitches(self):
        r_f = self.practice.reference_frequency
        _pitches = {
            "c-flat": r_f / 4 * 9 / 8,
            "c": r_f / 4 * 6 / 5,
            "c-sharp": r_f / 4 * 5 / 4, "d-flat": r_f / 4 * 5 / 4,
            "d": r_f / 4 * 4 / 3,
            "d-sharp": r_f / 4 * 45 / 32, "e-flat": r_f / 4 * 45 / 32,
            "e": r_f / 4 * 3 / 2,
            "f": r_f / 4 * 8 / 5,
            "f-sharp": r_f / 4 * 5 / 3, "g-flat": r_f / 4 * 5 / 3,
            "g": r_f / 4 * 9 / 5,
            "g-sharp": r_f / 4 * 15 / 8, "a-flat": r_f / 4 * 15 / 8,
            "a": r_f / 2,
            "a-sharp": r_f / 2 * 16 / 15, "b-flat": r_f / 2 * 16 / 15,
            "b": r_f / 2 * 9 / 8,
        }

        pitches = {}
        for n in range(4):
            add_on = ["", ""]
            for _ in range(n):
                add_on[0] += "'"
                add_on[1] += ","
            for name, ratio in _pitches.items():
                pitches[name + add_on[0]] = ratio * 2 ** n
                if n > 0:
                    pitches[name + add_on[1]] = ratio / (2 ** n)

        self.pitches = pitches

    def set_chords(self):

        scale_chords = [
            [(2, -1), (4, -1), (0, 0)],
            [(4, -1), (6, -1), (1, 0)],
            [(4, -1), (0, 0), (2, 0)],
            [(5, -1), (0, 0), (3, 0)],
            [(0, 0), (2, 0), (4, 0)],
            [(0, 0), (3, 0), (5, 0)],
            [(1, 0), (4, 0), (6, 0)]
        ]

        triad_chords = [
            [(2, -1), (4, -1), (0, 0)],
            [(4, -1), (0, 0), (2, 0)],
            [(0, 0), (2, 0), (4, 0)],
            [(2, 0), (4, 0), (0, 1)],
            [(4, 0), (0, 1), (2, 1)],
            [(0, 1), (2, 1), (4, 1)],
            [(2, 1), (4, 1), (0, 2)],
        ]

        kind = self.practice.music_key.split(' ')[-1]
        if kind != 'major':
            kind = 'melodic'

        groups = []
        if "Octave" in self.practice.exercise:
            n_oct = 1
            if 'Two' in self.practice.exercise:
                n_oct = 2

            up_chords = []
            down_chords = []
            for i_o in range(n_oct):
                for i_c, chord in enumerate(scale_chords):
                    up_chords.append([])
                    down_chords = [[], ] + down_chords
                    for note, octave in chord:
                        ratio = cst.PURE_RATIOS['up'][kind][note].split('/')
                        ratio = int(ratio[0]) / int(ratio[1])
                        rts = ratio * 2 ** (octave + i_o)
                        up_chords[-1].append(rts)
                        ratio = cst.PURE_RATIOS['down'][kind][note].split('/')
                        ratio = int(ratio[0]) / int(ratio[1])
                        rts = ratio * 2 ** (octave + i_o)
                        down_chords[0].append(rts)
            up_chords.append([r * 2 ** n_oct for r in up_chords[0]])
            groups.append(up_chords + down_chords)
        else:

            for n in range(3, 8):
                up_chords = []
                down_chords = []
                for i_c, chord in enumerate(triad_chords[:n]):
                    up_chords.append([])
                    down_chords = [[], ] + down_chords
                    for note, octave in chord:
                        ratio = cst.PURE_RATIOS['up'][kind][note].split('/')
                        ratio = int(ratio[0]) / int(ratio[1])
                        rts = ratio * 2 ** octave
                        up_chords[-1].append(rts)
                        ratio = cst.PURE_RATIOS['down'][kind][note].split('/')
                        ratio = int(ratio[0]) / int(ratio[1])
                        rts = ratio * 2 ** octave
                        down_chords[0].append(rts)
                down_chords.pop(0)  # up_chords.append([r * 2 ** (n-1) for r in up_chords[0]])
                groups.append(up_chords + down_chords)
        return groups
