import numpy as np
import os
import subprocess
import time

import streamlit as st
import constants as cst


class Audio:

    def __init__(self):

        self.is_valid = False

    def ping(self, size: int) -> np.ndarray:

        signal = np.zeros(size)
        t = np.linspace(0, size / cst.SAMPLE_RATE, size)
        signal += np.sin(2 * np.pi * t * 1000) * (1 - t / size * cst.SAMPLE_RATE) ** 1
        signal += np.sin(2 * np.pi * t * 2000) * (1 - t / size * cst.SAMPLE_RATE) ** 2
        signal += np.sin(2 * np.pi * t * 4000) * (1 - t / size * cst.SAMPLE_RATE) ** 4
        signal /= np.abs(signal).max()

        return signal / 10.0

    def pulsator(self, signal, size, t):

        _t = t % (size / cst.SAMPLE_RATE)
        amp = (1 - _t / size * cst.SAMPLE_RATE) ** 0.5 * (_t / size * cst.SAMPLE_RATE) ** 0.25
        signal[4*size:] *= (amp * 0.75) + 0.25
        return signal

    def n_beats_root_pitch(self):

        pa = st.session_state.pa
        n_q = sum(st.session_state.pa.total_durations) / 48
        assert n_q == int(n_q)
        n_beats = int(n_q * 4)

        signal = np.zeros(n_beats * 60 * cst.SAMPLE_RATE // pa.tempo)

        size = signal.size // n_beats
        ping_signal = self.ping(size)

        for i in range(4):
            signal[i*size:(i+1)*size] = ping_signal

        root_pitch = pa.key.split('-')[0].lower()
        root_frequency = cst.set_pitches(pa.reference_pitch)[root_pitch+',,']
        while root_frequency < 100.0:
            root_frequency *= 2

        return signal, n_beats, root_frequency, size

    def drone_root(self, fifth=False):

        pa = st.session_state.pa

        signal, n_beats, root_frequency, size = self.n_beats_root_pitch()

        t = np.linspace(0, (signal.size - 4 * size) / cst.SAMPLE_RATE, signal.size - 4 * size)

        for h in range(1, 5):
            signal[4*size:] += np.sin(2.0 * np.pi * t * root_frequency * h) / h ** 2

        if fifth:
            for h in range(1, 5):
                signal[4 * size:] += np.sin(2.0 * np.pi * t * root_frequency * h * 3/2) / h ** 2

        signal = self.pulsator(signal, size, t)

        signal /= np.abs(signal).max()
        signal *= (2 ** 15 - 1)

        pa.audio_signal = signal.astype(np.int16)

    def pure_chords(self):

        pa = st.session_state.pa
        signal, n_beats, root_frequency, size = self.n_beats_root_pitch()
        # number of data points per beat
        dp_per_beat = int(60.0 / pa.tempo * cst.SAMPLE_RATE + 0.5)
        pa.audio_signal = signal

        previous_duration = 0
        if pa.key[0].isupper():
            i = 4
            while i < len(pa.total_durations):
                if pa.total_durations[i] != previous_duration:
                    previous_duration = pa.total_durations[i]
                    sample_size = int(pa.total_durations[i] / 12 * dp_per_beat)
                    t = np.linspace(0, sample_size/cst.SAMPLE_RATE, sample_size)
                    part = np.zeros(sample_size)
                for j, c in enumerate(cst.PURE_CHORDS[pa.exercise]):
                    part *= 0
                    for h in range(1, 5):
                        for k, c_m in enumerate(c):
                            part += np.sin(2*np.pi * t * root_frequency * h * c_m) / h ** 2
                    start = sum(pa.total_durations[:i + j]) * dp_per_beat // 12
                    part = part / np.abs(part).max()
                    f = np.linspace(0, 1, 1000)
                    part[:1000] *= f
                    part[-1000:] *= f[::-1]
                    signal[start:start+part.size] = part
                i += j
                while previous_duration == pa.total_durations[i]:
                    i += 1
                    if i >= len(pa.total_durations):
                        break
        pa.audio_signal = np.int16(signal * (2**15-1))

    def update(self):

        pa = st.session_state.pa

        if self.is_valid:
            return

        if pa.acc_instr == cst.ACCOMPANY['GP']:
            subprocess.run(
                ['/usr/bin/timidity', '-Ow', f'./.tmp/{pa.basename}-1.midi', '-o', f'.assets/{pa.basename}.wav'])
        elif pa.acc_instr == cst.ACCOMPANY['DR']:
            self.drone_root(fifth=False)
        elif pa.acc_instr == cst.ACCOMPANY['DF']:
            self.drone_root(fifth=True)
        elif pa.acc_instr == cst.ACCOMPANY['PC']:
            self.pure_chords()

        self.is_valid = True
