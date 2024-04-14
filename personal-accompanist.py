import os
import time
import uuid
import streamlit as st

from scales import scales
import subprocess

from constants import HEAD, EVENT_VALUES, TRANSLATIONS

from widgets import place_widgets


def books():
    return f'''
\\book {{ 
  \\bookOutputName "{st.session_state.basename}"
  \\header{{ tagline = "" }}
  \\score {{
    << \\voice_one >>
    \\layout{{indent = 0}}
  }}
}}
\\book {{
  \\bookOutputName "{st.session_state.basename}"
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
    for i, t in enumerate(v_text):

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


def get_selected_scale(musickey):
    for scale in scales:
        if scale['musickey'] == musickey:
            return scale


def get_selected_exercise(scale):

    state = st.session_state

    for exercise in scale['exercises']:
        if exercise['exercise'] == state.exercise:
            # we add a break indicator ( a capital R is not part of the lilypond syntax)
            # at the end. This is used to indicator to complete the bar with rests if beats remain
            # after the music is finished. However, the 'R' can be added in the input from 'scales'
            if exercise['pitches'][-1] != 'R':
                exercise['pitches'] += ' R'
            return exercise


def tones_list(data, event_value, current_clef):

    # n_o_events is the number of music/midi events per bar
    # note_value is the one of 16 = 'sixteenth', 8 = 'eights', etc.
    # in most cases n_o_events=note_values but for triples
    # these values are different, e.g. 12 and 8 will give triplets of eights
    n_o_events, note_value = EVENT_VALUES[event_value]
    duration = 0

    # two strings to collect the lilypond code for two staves
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
                ff += TRANSLATIONS[f]
            v_text.append(f"{TRANSLATIONS[clef]}{ton}{note_value}{ff}{TRANSLATIONS[string]}")
            m_text.append(f"r{note_value}")
            duration += 48 // n_o_events
        else:
            v_text.append(f"r{note_value}")
            m_text.append(f"r{note_value}")
            duration += 48 // n_o_events
            while True:
                if duration % 48 == 0:
                    break
                v_text.append(f"r{note_value}")
                m_text.append(f"r{note_value}")
                duration += 48 // n_o_events

    v_text = add_slurs(v_text, n_o_events)

    if n_o_events == 12:
        v_text = add_triplets(v_text)

    return v_text, m_text


def get_data(exercise):

    # prepare an intermediate data set that is easier to work on

    data = {}
    for desig in ['pitches', 'fingers', 'clefs', 'strings']:
        data[desig] = exercise[desig].split()
        while len(data['pitches']) > len(data[desig]):
            data[desig].append('-')
    return data


def create_voices(exercise):

    state = st.session_state
    mk = state.musickey

    # start of each staff definition
    current_clef = 'B'
    v_one = f'''voice_one = 
\\new Staff \\with {{midiInstrument = "acoustic grand" }} \\relative c, {{ {TRANSLATIONS[current_clef]} '''
    metronome = '''metronome = \\new Staff \\with {midiInstrument = "woodblock"} {'''
    v_one += f'  \\tempo 4={state.tempo}\n'

    v_one += '  \\key ' + mk.split('-')[0].lower() + ' \\' + mk.split('-')[1].lower() + '\n'
    v_one += 'r1'
    pitch = mk.split('-')[0].lower()
    metronome += f"{pitch}4 {pitch}4 {pitch}4 {pitch}4"

    data = get_data(exercise)
    for speed in sorted(state.speeds):
        for v, m in zip(*tones_list(data, speed, current_clef)):
            v_one += f" {v}"
            metronome += f" {m}"
        v_one += ' \\bar  "||"\n'

    v_one = v_one[:-3] + '.' + v_one[-2:]
    v_one += "}\n"
    metronome += "}\n"

    return v_one, metronome


def create_lilypond():

    state = st.session_state

    musickey = state.musickey.split('-')[0]

    scale = get_selected_scale(musickey)
    exercise = get_selected_exercise(scale)

    voice_one, metronome = create_voices(exercise)

    output = HEAD + voice_one + '\n' + metronome
    output += books()
    output = final_touches(output)

    with open(state.basename+'.ly', 'w') as fd:
        fd.write(output)


def create_assets():

    state = st.session_state

    subprocess.run(['lilypond',
                    '--silent', '-dno-point-and-click', '--svg', f'{state.basename}.ly'])
    subprocess.run(['inkscape',
                    f'{state.basename}.svg', f'--export-filename={state.basename}.svg', '--export-area-drawing'])

    os.renames(f'{state.basename}.svg', f'assets/{state.basename}.svg')
    subprocess.run(['/usr/bin/timidity', '-Ow', state.basename + '-1.midi', '-o', f'assets/{state.basename}.wav'])

    # clean up
    os.remove(f'{state.basename}-1.midi')
    os.remove(f'{state.basename}.ly')

    content = os.listdir('assets')
    # print(content)
    for entry in content:
        file = 'assets/' + entry
        file_time = os.path.getmtime(file)
        # Check against 2 hours
        if (time.time() - file_time)  > 7200:
            os.remove(file)


def init_session_variables():

    state = st.session_state

    if 'basename' not in state:
        state.basename = uuid.uuid4().hex


def main():

    init_session_variables()
    st.set_page_config(layout="wide")

    if 'musickey' in st.session_state:
        if st.session_state.speeds:
            create_lilypond()
            create_assets()

    place_widgets()


if __name__ == "__main__":
    main()
