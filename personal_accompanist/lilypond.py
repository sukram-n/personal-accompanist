from importlib import reload
import subprocess

import streamlit as st

import constants as cst

reload(cst)


def books():
    return f'''
\\book {{ 
  \\bookOutputName "{st.session_state.pa.basename}"
  \\header{{ tagline = "" }}
  \\score {{
    << \\voice_one >>
    \\layout{{indent = 0}}
  }}
}}
\\book {{
  \\bookOutputName "{st.session_state.pa.basename}"
  \\header {{ tagline = "" }}
  \\score {{
    << 
      \\metronome
      \\voice_one
    >>
    \\midi {{ }} 
  }}
}}
'''


def add_slurs(v_text, tempo):
    slur_is_open = False
    for i, t in enumerate(v_text[:-1]):

        if i % tempo == 0 and i < len(v_text) - 1 and not slur_is_open:
            v_text[i] += "\\("
            slur_is_open = True
        if slur_is_open and (i % tempo == tempo - 1 or v_text[i + 1].startswith("r")):
            v_text[i] += "\\)"
            slur_is_open = False
    if slur_is_open:
        v_text.append('}')
    return v_text


def add_triplets(v_text):

    triplet_is_open = False
    for i in range(len(v_text) - 1):
        if i % 3 == 0 and not triplet_is_open:
            v_text[i] = "\n\\tuplet 3/2 {" + v_text[i]
            triplet_is_open = True
        if i % 3 == 2 and triplet_is_open:
            v_text[i] += "}"
            triplet_is_open = False
    if triplet_is_open:
        v_text[-1] += "}"
    return v_text


def final_touches(output):

    # not really necessary but makes the lilypond code look a bit nicer to read

    output = output.replace('\n', ' ')

    while '  ' in output:
        output = output.replace('  ', ' ')

    # clean up and combination of rests
    output = output.replace('\\tuplet 3/2 {r8 r8 r8}', 'r4')
    # the replacements are done from back to front
    rs = ['61r', '8r', '4r', '2r', '1r']
    for n, r in zip(rs[:-1], rs[1:]):
        output = output[::-1].replace(f'{n} {n} ', f'{r} ')[::-1]

    # remove slurs without length, easier to clean than to care for while setting them, ;-)
    output = output.replace('\\(\\)', '')

    # put back some line breaks
    output = output.replace('}', '}\n')
    output = output.replace('\\new', '\n\\new')
    output = output.replace('\\relative', '\n\\relative')
    output = output.replace('\\key', '\n\\key')
    output = output.replace('>>', '>>\n')
    output = output.replace('\\bar "||"', '\\bar "||"\n')
    output = output.replace('\\bar "|."', '\\bar "|."\n')

    return output


def get_data(scale):

    # prepare an intermediate data set that is easier to work on

    data = {}
    for desig in ['pitches', 'fingers', 'clefs', 'strings']:
        data[desig] = scale[desig].split()
        data[desig] = [item.strip() for item in data[desig]]
        if desig == 'pitches':
            if data[desig][-1] != 'R':
                data[desig].append('R')
        while len(data['pitches']) > len(data[desig]):
            data[desig].append('-')
    if data['pitches'][-1] != 'R':
        data['pitches'].append('R')
    return data


def tones_list(data, event_value, current_clef):

    # n_o_events is the number of music/midi events per bar
    # note_value is the one of 16 = 'sixteenth', 8 = 'eights', etc.
    # in most cases n_o_events=note_values but for triples
    # these values are different, e.g. 12 and 8 will give triplets of eights
    n_o_events, note_value = cst.EVENT_VALUES[event_value]
    durations = []
    # two lists to collect the lilypond code for two staves
    # v_text is for the music and m_text records events for indicating the speed at the beginning,
    # in general four beats on a woodblock
    v_text = []
    m_text = []

    for ton, finger, clef, string in zip(
            data['pitches'],
            data['fingers'],
            data['clefs'],
            data['strings']):
        if current_clef != clef and clef != '-':
            current_clef = clef
        else:
            clef = '-'
        if ton != "R":
            ff = ""
            for f in finger:
                ff += cst.TRANSLATIONS[f]
            v_text.append(f"{cst.TRANSLATIONS[clef]}{ton}{note_value}{ff}{cst.TRANSLATIONS[string]}")
        else:
            v_text.append(f"r{note_value}")

        m_text.append(f"r{note_value}")
        durations.append(48 // n_o_events)

        if ton == 'R':
            while sum(durations) % 48 != 0:
                v_text.append(f"r{note_value}")
                m_text.append(f"r{note_value}")
                durations.append(48 // n_o_events)

    v_text = add_slurs(v_text, n_o_events)

    if n_o_events == 12:
        v_text = add_triplets(v_text)

    return v_text, m_text, durations


def create_voices(exercise):

    pa = st.session_state.pa
    mk = pa.key
    # start of each staff definition
    current_clef = 'B'
    v_one = 'voice_one = \\new Staff \\with {midiInstrument = "acoustic grand" } {\n'
    v_one += '\\accidentalStyle modern-cautionary \n'
    text = pa.key_text.replace("-", " \\").lower()
    v_one += f'  \\key {text}\n'
    v_one += f' {{ {cst.TRANSLATIONS[current_clef]}'
    v_one += f'  \\tempo 4={int(pa.tempo)} \n'
    metronome = '''metronome = \\new Staff \\with {midiInstrument = "woodblock"} {'''

    v_one += 'r1'
    metronome += f"{mk.lower()}4 {mk.lower()}4 {mk.lower()}4 {mk.lower()}4"
    pa.total_durations = [12, 12, 12, 12]

    data = get_data(exercise)
    for speed in sorted(pa.speeds):
        _v_one, _metro, _durations = tones_list(data, speed, current_clef)
        pa.total_durations += _durations
        for v, m in zip(_v_one, _metro):
            v_one += f" {v}"
            metronome += f" {m}"
        v_one += ' \\bar  "||"\n'

    v_one = v_one[:-3] + '.' + v_one[-2:]
    v_one += "}\n}\n"
    metronome += "}\n"

    return v_one, metronome


class LilyPond:

    def __init__(self):
        self.is_valid = False

        self.output = ""

    def update(self):

        if self.is_valid:
            return

        pa = st.session_state.pa

        # musickey = state.musickey.split('-')[0]

        scale = cst.SCALES[pa.key][pa.exercise]
        voice_one, metronome = create_voices(scale)

        self.output = cst.HEAD + voice_one + '\n' + metronome
        self.output += books()
        self.output = final_touches(self.output)

        with open(f'./.tmp/{pa.basename}.ly', 'w') as fd:
            fd.write(self.output)

        result = subprocess.run(
            ['lilypond', '--silent', '-dno-point-and-click', '--svg', '--output=./.tmp', f'./.tmp/{pa.basename}.ly'])

        if result.returncode != 0:
            return result.returncode

        result = subprocess.run(
            ['inkscape',
             f'./.tmp/{pa.basename}.svg', f'--export-filename=./.assets/{pa.basename}.svg',
             '--export-area-drawing'])
        if result.returncode != 0:
            return result.returncode

        self.is_valid = True
        return 0
