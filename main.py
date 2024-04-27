import os
import time

import streamlit as st

import personal_accompanist


def init_session() -> personal_accompanist.PersonalAccompanist:

    st.set_page_config(layout="wide")

    for folder in ['./.tmp', './.assets']:
        if not os.path.exists(folder):
            os.mkdir(folder)

    if 'pa' not in st.session_state:
        # if keep our stuff in a separate class instance to avoid
        # name space conflicts
        st.session_state.pa = personal_accompanist.PersonalAccompanist()

    return st.session_state.pa


def clean_up():

    pa = st.session_state.pa
    # clean up

    for file in [f'.tmp/{pa.basename}.ly', f'.tmp/{pa.basename}-1.midi']:
        if os.path.exists(file) and False:
            os.remove(file)

    for folder, age in [('./.tmp', 18), ('./.assets', 600)]:
        content = os.listdir(folder)
        # print(content)
        for entry in content:
            file = f'{folder}/{entry}'
            file_time = os.path.getmtime(file)
            # Check against 2 hours, remove older stuff
            if (time.time() - file_time) > age:
                os.remove(file)


def main():

    pa = init_session()
    ss = st.session_state

    if not pa.initial_run:

        if 'loop' in ss:
            pa.loop = ss.loop

        if ss.exercise != pa.exercise:
            pa.lilypond.is_valid &= False
            pa.audio.is_valid &= False
            pa.exercise = ss.exercise

        if ss.musickey != pa.key_text:
            pa.lilypond.is_valid &= False
            pa.audio.is_valid &= False
            pa.key = ss.musickey.split('-')[0]

        if ss.tempo != pa.tempo:
            pa.lilypond.is_valid &= False
            pa.audio.is_valid &= False
            pa.tempo = ss.tempo

        if sorted(ss.speeds) != pa.speeds:
            pa.lilypond.is_valid &= False
            pa.audio.is_valid &= False
            pa.speeds = sorted(ss.speeds)

        if ss.acc_instr != pa.acc_instr:
            pa.audio.is_valid &= False
            pa.acc_instr = ss.acc_instr

    pa.lilypond.update()

    pa.audio.update()

    pa.widgets.update()

    pa.initial_run = False

    clean_up()


if __name__ == "__main__":

    main()
