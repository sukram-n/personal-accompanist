import streamlit as st
from practice_data import practice_data, constants as cst

EXERCISES = ['One Octave', 'Two Octaves', 'Triads']

SPEEDS = {
    '11/1 notes': (1, 1),
    '21/2 notes': (2, 2),
    '31/4 notes': (4, 4),
    '41/8 notes': (8, 8),
    '51/8 triplets': (12, 8),
    '61/16 notes': (16, 16)
}


class Practices:

    def __init__(self):

        self.music_key = 'c major'
        self.speeds = [[s for s in SPEEDS][0], ]
        self.tempo = 60
        self.exercise = 'One Octave'
        self.has_changed: bool = True
        self.acc_instr = cst.ACCOMPANY['GP']
        self.loop = False
        self.slurs = True

    def get_data(self):

        # prepare an intermediate data set that is easier to work on

        exercise = practice_data[self.music_key][self.exercise]
        data = {}
        for desig in exercise:
            data[desig] = exercise[desig].split()
            data[desig] = [item.strip() for item in data[desig]]
            if desig == 'pitches':
                if data[desig][-1] != 'R':
                    data[desig].append('R')
            while len(data['pitches']) > len(data[desig]):
                data[desig].append('-')
        return data

    def update_variables(self):

        ss = st.session_state

        if 'loop' in ss:
            self.loop = ss.loop

        if ss.slurs != self.slurs:
            self.slurs = ss.slurs
            self.has_changed = True

        if ss.exercise != self.exercise:
            self.exercise = ss.exercise
            self.has_changed = True

        if ss.musickey != self.music_key:
            self.has_changed = True
            self.music_key = ss.musickey

        if ss.tempo != self.tempo:
            self.has_changed = True
            self.tempo = ss.tempo

        if sorted(ss.speeds) != self.speeds:
            self.has_changed = True
            self.speeds = sorted(ss.speeds)

        if ss.acc_instr != self.acc_instr:
            self.has_changed = True
            self.acc_instr = ss.acc_instr
