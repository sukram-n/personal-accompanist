import os
import streamlit as st
from scales import scales
from constants import EXERCISES, EVENT_VALUES


def format_func(s: str) -> str:

    return s[1:]


def place_widgets():

    state = st.session_state

    st.write('## Private Accompanist')

    musickeys = []
    for scale in scales:
        k = scale['musickey']
        if k.islower():
            musickeys.append(k + '-minor')
        else:
            musickeys.append(k + '-major')

    sidebar = st.sidebar
    settings, about = sidebar.tabs(['Settings', 'About'])
    settings.selectbox('Choose key', musickeys, key='musickey', index=0)
    settings.selectbox('Exercise', EXERCISES, key='exercise')
    settings.slider('Tempo (b.p.m.)', 30, 240, step=5, key='tempo')
    settings.multiselect('Value of notes', EVENT_VALUES, format_func=format_func, key='speeds')

    if 'loop' in state:
        loop = state.loop
    else:
        loop = False

    # check for file existance before showing them
    if (os.path.exists(f'assets/{state.basename}.svg') and
            os.path.exists(f'assets/{state.basename}.wav') and
            st.session_state.speeds):
        # the sheet music

        st.image(f'assets/{state.basename}.svg', use_column_width='always')
        # the audio file
        st.audio(f'assets/{state.basename}.wav', loop=loop)
        st.checkbox('Loop', key='loop')
    else:
        st.write('Choose settings in sidebar')

