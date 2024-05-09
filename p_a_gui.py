import os

import streamlit as st

from scales_and_triads_data import data as sat_data
import p_a_constants as cst

from p_a_scales_and_triads import Exercises, EXERCISE_TYPE, SPEEDS
from p_a_audio import Audio
from p_a_lilypond import Lilypond


def format_func(s: str) -> str:
    return s[1:]


def scales_and_triads_tab(sat):
    state = st.session_state

    if 'musickeys' not in state:
        musickeys = []
        for key, _exercises in sat_data.items():
            musickeys.append(key)
        state['musickeys'] = musickeys

    cols = sat.columns(2)
    cols[0].selectbox('Exercise', EXERCISE_TYPE, key='exercise')

    cols[1].selectbox('Choose Key', state.musickeys, key='musickey', index=0)

    sat.slider('Tempo (b.p.m.)', 30, 240, step=5, key='tempo', value=60)

    sat.multiselect('Value of Notes', SPEEDS, format_func=format_func, key='speeds',
                    default='31/4 notes')

    acc_instr = [_e for _k, _e in cst.ACCOMPANY.items()]
    sat.selectbox('Accompanying Instrument', acc_instr, key='acc_instr', index=0)

    disabled = False
    if state.p_a.exercises.acc_instr == cst.ACCOMPANY['GP']:
        disabled = True

    sat.slider('Reference a at (Hz)',
               438.0, 448.0, step=0.5, value=443.0, key='reference_frequency', disabled=disabled)

    cols = sat.columns(2)
    cols[0].checkbox('Slurs', key='slurs')
    cols[1].checkbox('Fingerings', key='fingerings')


def make_sidebar():
    sidebar = st.sidebar
    scales_and_trials, about = sidebar.tabs(['Scales and Triads', 'About'])

    scales_and_triads_tab(scales_and_trials)


class GUI:

    def __init__(self,
                 basename: str,
                 practice: Exercises | None = None,
                 lilypond: Lilypond | None = None, audio: Audio = None):

        self.basename = basename
        self.practice = practice
        self.lilypond = lilypond
        self.audio = audio
        # self.is_valid = False

    def show_gui(self):

        p_a = st.session_state.p_a

        st.write('## Personal Accompanist')

        make_sidebar()

        # check for file existance before showing them
        if os.path.exists(f'.assets/{self.basename}.svg'):
            # the sheet music
            st.image(f'.assets/{self.basename}.svg', use_column_width='always')

        if os.path.exists(f'.assets/{self.basename}.wav'):

            cols = st.columns([0.9, 0.1])
            # the audio file
            if st.session_state.p_a.exercises.acc_instr == cst.ACCOMPANY['GP']:
                cols[0].audio(f'.assets/{self.basename}.wav', loop=p_a.exercises.loop)
            else:
                cols[0].audio(self.audio.signal, loop=p_a.exercises.loop, sample_rate=cst.SAMPLE_RATE)
            cols[1].checkbox('Loop', key='loop')

        # self.is_valid = True
