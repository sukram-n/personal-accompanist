import os

import numpy as np
import streamlit as st

import constants as cst


def create_sound():

    sample_rate = 44100.0
    f = 443/8*3/4 * 9/8
    dt = 4.0
    t = np.linspace(0.0, dt, int(sample_rate*dt))
    sound = np.zeros_like(t)
    for n, a in enumerate([1, 0.1, 0.01, 0.01, 0.005, 0.001, 0.0005]):
        sound += a * np.sin(2.0 * np.pi * (n + 1.0) * f * t + a)
        # sound += a * np.sin(2.0 * np.pi * (n + 1.0) * f * t * 3. / 2. + a)
    sound /= np.abs(sound).max()
    sound = np.int16(sound*(2.0 ** 15.0 - 10.0) * ((dt-t)/dt)**0.5)
    return sound, sample_rate


def format_func(s: str) -> str:

    return s[1:]


def make_sidebar():

    state = st.session_state

    if 'musickeys' not in state:
        musickeys = []
        for key, exercises in cst.SCALES.items():
            present = False
            for _key, exer in exercises.items():
                if len(exer['pitches']):
                    if key[0].islower():
                        musickeys.append(key + '-minor')
                    else:
                        musickeys.append(key + '-major')
                    break
        state['musickeys'] = musickeys

    sidebar = st.sidebar
    settings, about = sidebar.tabs(['Settings', 'About'])

    settings.selectbox('Exercise', cst.EXERCISES, key='exercise')

    settings.selectbox('Choose Key', state.musickeys, key='musickey', index=0)

    settings.slider('Tempo (b.p.m.)', 30, 240, step=5, key='tempo')

    settings.multiselect('Value of Notes', cst.EVENT_VALUES, format_func=format_func, key='speeds')

    acc_instr = [_e for _k, _e in cst.ACCOMPANY.items()]
    settings.selectbox('Accompanying Instrument', acc_instr, key='acc_instr', index=0)


class Widgets:

    def __init__(self):
        self.is_valid = False

    def update(self):

        pa = st.session_state.pa

        st.write('## Personal Accompanist')

        make_sidebar()

        # check for file existance before showing them
        if (os.path.exists(f'.assets/{pa.basename}.svg') and
                os.path.exists(f'.assets/{pa.basename}.wav') and
                st.session_state.speeds):

            # the sheet music
            st.image(f'.assets/{pa.basename}.svg', use_column_width='always')
            # the audio file
            if st.session_state.pa.acc_instr == cst.ACCOMPANY['GP']:
                st.audio(f'.assets/{pa.basename}.wav', loop=pa.loop)
            else:
                st.audio(pa.audio_signal, loop=pa.loop, sample_rate=cst.SAMPLE_RATE)
            # sound, s_rate = create_sound()
            # st.audio(sound, sample_rate=s_rate, loop=loop)
            st.checkbox('Loop', key='loop')
        else:
            st.write('Choose settings in sidebar')

        self.is_valid = True
