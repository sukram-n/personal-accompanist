import os
import subprocess

import p_a_constants as cst

from p_a_practice import SPEEDS, Practices

TRANSLATIONS = {
    "0": "^\\Nf",
    "1": "^\\If",
    "2": "^\\Mf",
    "3": "^\\Rf",
    "4": "^\\Pf",
    "t": "^\\Tf",
    "-": "",
    "B": '\\clef "bass_8"\n',
    "T": '\\clef "tenor_8"\n',
    "V": '\\clef "violin_8"\n',
    "G": '_\\Gstring ',
    "D": '_\\Dstring ',
    "A": '_\\Astring ',
    "E": '_\\Estring ',
}

HEAD = f"""\\version "{cst.LILYPOND_VERSION}"
\\language "english"
\\include "./../lilypond/commons.ly"

"""


class Staff:

    def __init__(self):

        self.list = []
        self.source = ''
        self.has_changed = True

    def append(self, t: str):
        self.list.append(t)
        self.has_changed = True

    def concatenate(self, t: str):
        self.source += t
        self.has_changed = True

    def add_triplets(self) -> None:

        triplet_is_open = False
        for i in range(len(self.list) - 1):
            if i % 3 == 0 and not triplet_is_open:
                self.list[i] = " \\tuplet 3/2 {" + self.list[i]
                triplet_is_open = True
            if i % 3 == 2 and triplet_is_open:
                self.list[i] += "}"
                triplet_is_open = False
        if triplet_is_open:
            self.list[-1] += "}"

    def add_slurs(self, tempo) -> None:
        slur_is_open = False
        i = 0
        for i, t in enumerate(self.list[:-1]):

            if i % tempo == 0 and i < len(self.list) - 1 and not slur_is_open:
                self.list[i] += "\\("
                slur_is_open = True
            if slur_is_open and (i % tempo == tempo - 1 or self.list[i + 1].startswith("r")):
                self.list[i] += "\\)"
                slur_is_open = False
        if slur_is_open:
            self.list[i] += '\\)'

    def collect_rests(self):
        # clean up and combination of rests
        while '  ' in self.source:
            self.source = self.source.replace('  ', ' ')
        self.source = self.source.replace('\\tuplet 3/2 {r8 r8 r8}', 'r4')
        # the replacements are done from back to front
        rs = ['61r', '8r', '4r', '2r', '1r']
        replaced_something = True
        while replaced_something:
            replaced_something = False
            for n, r in zip(rs[:-1], rs[1:]):
                new = self.source[::-1].replace(f'{n} {n} ', f'{r} ')[::-1]
                if new != self.source:
                    replaced_something = True
                    self.source = new
                    break
        # remove slurs without length, easier to clean than to care for while setting them, ;-)
        self.source = self.source.replace('\\(\\)', '')


class Staves:

    def __init__(self, practice):

        self.practice = practice
        self.piano = Staff()
        self.metronome = Staff()

    @property
    def has_changed(self):
        return self.piano.has_changed or self.metronome.has_changed

    def append(self, p_t: str, m_t: str):
        self.piano.append(p_t)
        self.metronome.append(m_t)

    def concatenate(self, p_t: str, m_t: str):
        self.piano.concatenate(p_t)
        self.metronome.concatenate(m_t)

    def tones_list(self, data, speed_value, current_clef):
        # n_o_events is the number of music/midi events per bar
        # note_value is the one of 16 = 'sixteenth', 8 = 'eights', etc.
        # in most cases n_o_events=note_values but for triples
        # these values are different, e.g. 12 and 8 will give triplets of eights
        n_o_events, note_value = SPEEDS[speed_value]
        durations = [[]]
        # two lists to collect the lilypond code for two staves
        # piano is for the music and metronome records events for indicating the speed at the beginning,
        # in general four beats on a woodblock

        staves = Staves(self.practice)
        for ton, finger, clef, string in zip(
                data['pitches'], data['fingers'], data['clefs'], data['strings']):
            if current_clef != clef and clef != '-':
                current_clef = clef
            else:
                clef = '-'
            if ton != "R":
                ff = ""
                if self.practice.show_fingerings:
                    for f in finger:
                        ff += TRANSLATIONS[f]
                else:
                    string = '-'

                text = f"{TRANSLATIONS[clef]}{ton}{note_value}{ff}{TRANSLATIONS[string]}"
                staves.append(text, f"r{note_value}")
                durations[-1].append(48 // n_o_events)
            else:
                staves.append(f"r{note_value}", f"r{note_value}")
                durations.append([-48 // n_o_events, ])

                while sum([sum([abs(_d) for _d in d]) for d in durations]) % 48 != 0:
                    staves.append(f"r{note_value}", f"r{note_value}")
                    durations[-1].append(-48 // n_o_events)
                durations.append([])

        if len(durations[-1]) == 0:
            durations.pop(-1)

        if self.practice.show_slurs:
            staves.piano.add_slurs(n_o_events)

        if n_o_events == 12:
            staves.piano.add_triplets()

        for v, m in zip(staves.piano.list, staves.metronome.list):
            staves.concatenate(f" {v} ", f" {m} ")

        return staves, durations

    def update(self):

        current_clef = 'B'
        # start of each staff definition
        self.piano.source = 'piano = \\new Staff \\with {midiInstrument = "acoustic grand" } {\n'
        self.metronome.source = 'metronome = \\new Staff \\with {midiInstrument = "woodblock" } {\n'

        text = self.practice.music_key.replace(" ", " \\").lower()
        self.piano.concatenate('  \\accidentalStyle modern-cautionary\n'
                               '  \\tupletDown\n'
                               '  \\override TextScript.staff-padding = # 3\n')

        self.piano.concatenate(f'  \\key {text}\n'
                               f'  {TRANSLATIONS[current_clef]}'
                               f'  \\tempo 4={self.practice.tempo} \n'
                               'r1')

        self.metronome.concatenate("c4 c4 c4 c4 \n")
        durations = [[12, 12, 12, 12]]

        # ---------------------------------------------------------------------
        data = self.practice.get_data()

        bar = ''
        for speed in sorted(self.practice.speeds):
            staves, _durations = self.tones_list(data, speed, current_clef)
            durations += _durations
            self.concatenate(bar, bar)
            self.concatenate(staves.piano.source, staves.metronome.source)
            bar = ' \\bar  "||"\n'

        if self.practice.loop:
            bar = " \\set Score.repeatCommands = #'(end-repeat) \n"
        else:
            bar = ' \\bar  "|."\n'

        self.concatenate(bar, bar)

        # ---------------------------------------------------------------------
        # finally:
        self.concatenate("\n}\n", "\n}\n")

        self.piano.collect_rests()

        return durations


class Lilypond:

    def __init__(self, basename: str, practice: Practices):

        self.basename = basename
        self.practice = practice
        self.durations = None
        self.footer: str = ""

        self.staves = Staves(self.practice)

        self._svg_source: str = ''
        self._mid_source: str = ''
        self._source: str = ''
        self._destination = ''

    # ToDo:
    # recalculate only if necessary
    # @property
    # def is_valid(self):
    #   return self._is_valid and not self.exercise.has_changed

    @property
    def total_duration(self):
        s = [sum([abs(_d) for _d in d]) for d in self.durations]
        s = sum(s)
        return s

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, dest):
        if dest != self._destination:
            self._destination = dest
            self._update_footer()

    @property
    def source(self):

        if self.staves.has_changed:
            self.durations = self.staves.update()

        source = HEAD
        source += self.staves.piano.source
        source += self.staves.metronome.source
        source += self.footer

        return source

    def _update_footer(self) -> None:

        self.footer = f'\n\\book {{\n  \\bookOutputName "{self.destination}_{self.basename}"\n'
        self.footer += '  \\header{ tagline = "" }\n  \\score {\n'
        if self.destination == 'svg':
            self.footer += '    << \\piano >>\n'
            self.footer += '    \\layout{ indent = 0 }\n'
        if self.destination == 'midi':
            self.footer += '    <<\n        \\piano\n        \\metronome\n      >>\n    \\midi { }\n'
        self.footer += '  }\n}'

    @staticmethod
    def final_touches(output):
        # not really necessary but makes the lilypond code look a bit nicer to read

        output = output.replace('\n', ' ')

        while '  ' in output:
            output = output.replace('  ', ' ')

        # put back some line breaks
        output = output.replace('}', '}\n')
        output = output.replace('\\new', '\n\\new')
        output = output.replace('\\relative', '\n\\relative')
        output = output.replace('\\key', '\n\\key')
        output = output.replace('>>', '>>\n')
        output = output.replace('\\bar "||"', '\\bar "||"\n')
        output = output.replace('\\bar "|."', '\\bar "|."\n')

        return output

    def compile(self, destination='svg'):

        self.destination = destination
        file_name = f'./.lilypond/{destination}_{self.basename}.ly'
        with open(file_name, 'w') as file:
            file.write(self.source)

        dest = ''
        if destination == 'svg':
            dest = '--svg'
        subprocess.run(
            ['lilypond', '--silent', '-dno-point-and-click', dest, '--output=./.lilypond',
             file_name])

        # os.remove(file_name)

    def prepare(self):

        #if not self.practice.has_changed:
        #    return

        self.compile('svg')

        # trim svg
        subprocess.run(
            ['inkscape',
             f'./.lilypond/svg_{self.basename}.svg', f'--export-filename=./.assets/{self.basename}.svg',
             '--export-area-drawing'])
