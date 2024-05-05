import os

import streamlit as st

from practice_data import practice_data, constants as cst

from p_a_practice import Practices, EXERCISES, SPEEDS
from p_a_audio import Audio
from p_a_lilypond import Lilypond

import p_a


def format_func(s: str) -> str:
    return s[1:]


def make_sidebar():
    state = st.session_state

    if 'musickeys' not in state:
        musickeys = []
        for key, _exercises in practice_data.items():
            musickeys.append(key)
        state['musickeys'] = musickeys

    sidebar = st.sidebar
    settings, about = sidebar.tabs(['Settings', 'About'])

    cols = settings.columns(2)
    cols[0].selectbox('Exercise', EXERCISES, key='exercise')

    cols[1].selectbox('Choose Key', state.musickeys, key='musickey', index=0)

    settings.slider('Tempo (b.p.m.)', 30, 240, step=5, key='tempo', value=60)

    cols = settings.columns([0.7, 0.3])
    cols[0].multiselect('Value of Notes', SPEEDS, format_func=format_func, key='speeds',
                        default='31/4 notes')
    cols[1].checkbox('Slurs', key='slurs')

    acc_instr = [_e for _k, _e in cst.ACCOMPANY.items()]
    settings.selectbox('Accompanying Instrument', acc_instr, key='acc_instr', index=0)


class GUI:

    def __init__(self,
                 practice: Practices | None = None,
                 lilypond: Lilypond|None=None, audio: Audio = None):
        self.practice = practice
        self.lilypond = lilypond
        self.audio = audio
        # self.is_valid = False

    def show_gui(self):

        p_a: p_a.PersonalAccompanist = st.session_state.p_a

        st.write('## Personal Accompanist')

        make_sidebar()

        # check for file existance before showing them
        if os.path.exists('.assets/personal_accompanist.svg'):
            # the sheet music
            st.image(f'.assets/personal_accompanist.svg', use_column_width='always')

        if os.path.exists('.assets/personal_accompanist.wav'):

            cols = st.columns([0.9, 0.1])
            # the audio file
            if st.session_state.p_a.practice.acc_instr == cst.ACCOMPANY['GP']:
                cols[0].audio('.assets/personal_accompanist.wav', loop=p_a.practice.loop)
            else:
                cols[0].audio(self.audio.signal, loop=p_a.practice.loop, sample_rate=cst.SAMPLE_RATE)
            cols[1].checkbox('Loop', key='loop')

        # self.is_valid = True
