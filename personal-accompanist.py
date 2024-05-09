import os
import time

import streamlit as st

from p_a import PersonalAccompanist


def init_session() -> PersonalAccompanist:

    st.set_page_config(layout="wide")

    for folder in ['./.lilypond', './.assets']:
        if not os.path.exists(folder):
            os.mkdir(folder)

    st.session_state.p_a = PersonalAccompanist()

    return st.session_state.p_a


def clean_up() -> None:

    """
    remove old files
    """

    # delete everything that is older than 600 seconds in the `./.tmp` folder
    # and older the two hours in the `./.assets` folder
    for folder, age in [('./.lilypond', 600), ('./.assets', 7200)]:
        content = os.listdir(folder)
        # print(content)
        for entry in content:
            file = f'{folder}/{entry}'
            file_time = os.path.getmtime(file)
            if (time.time() - file_time) > age:
                os.remove(file)


def main():

    rerun = False

    if "p_a" not in st.session_state:
        # ok, then this is the initial run
        # Prepare the app session with class instances and variables.
        # We keep our stuff in an own class instance to avoid name space conflicts
        # this instance is stored in `st.sessionstate.p_a`

        p_a = init_session()
        rerun = True

    else:

        p_a = st.session_state.p_a

        p_a.exercises.update_variables()
        p_a.lilypond.prepare()
        p_a.audio.prepare()

    p_a.gui.show_gui()

    clean_up()
    if rerun:
        st.rerun()


if __name__ == "__main__":

    main()
