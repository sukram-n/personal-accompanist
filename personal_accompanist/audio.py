import subprocess

import numpy as np

import streamlit as st
from .practice import Practices
from practice_data import constants as cst


class Audio:

    def __init__(self, practice: Practices):

        self.practice = practice
        self.signal: np.ndarray | None = None
        self.loop: bool = False
        self.acc_instr = cst.ACCOMPANY['GP']
        self.is_valid: bool = False

    def prepare(self):

        p_a = st.session_state.p_a

        if self.practice.acc_instr == cst.ACCOMPANY['GP']:
            p_a.lilypond.compile('midi')
            subprocess.run(
                ['/usr/bin/timidity', '-Ow', './lilypond/midi_personal_accompanist.midi', '-o',
                 '.assets/personal_accompanist.wav'])

        elif self.practice.acc_instr == cst.ACCOMPANY['DR']:
            self.drone_root(fifth=False)
        elif self.practice.acc_instr == cst.ACCOMPANY['DF']:
            self.drone_root(fifth=True)
        elif self.practice.acc_instr == cst.ACCOMPANY['PC']:
            self.pure_chords()

        self.is_valid = True

    @staticmethod
    def ping(size: int) -> np.ndarray:

        signal = np.zeros(size)
        t = np.linspace(0, size / cst.SAMPLE_RATE, size)
        signal += np.sin(2 * np.pi * t * 1000) * (1 - t / size * cst.SAMPLE_RATE) ** 1
        signal += np.sin(2 * np.pi * t * 2000) * (1 - t / size * cst.SAMPLE_RATE) ** 2
        signal += np.sin(2 * np.pi * t * 4000) * (1 - t / size * cst.SAMPLE_RATE) ** 4
        signal /= np.abs(signal).max()

        return signal / 50.0

    @staticmethod
    def pulsator(signal, size, t):

        _t = t % (size / cst.SAMPLE_RATE)
        amp = (1 - _t / size * cst.SAMPLE_RATE) ** 0.5 * (_t / size * cst.SAMPLE_RATE) ** 0.25
        amp = (amp - amp.min()) / (amp.max() - amp.min())
        amp = np.maximum(0, amp - 0.1) / 0.9
        amp = amp ** 2
        signal[4 * size:] *= (amp * 0.75) + 0.25
        return signal

    def n_beats_root_pitch(self):

        p_a = st.session_state.p_a
        assert p_a.lilypond.total_duration % 48 == 0
        n_q = p_a.lilypond.total_duration // 48
        n_beats = n_q * 4

        signal = np.zeros(n_beats * 60 * cst.SAMPLE_RATE // self.practice.tempo)

        size = signal.size // n_beats
        ping_signal = self.ping(size)

        for i in range(4):
            signal[i * size:(i + 1) * size] = ping_signal

        root_pitch = self.practice.music_key.split(' ')[0]
        root_frequency = p_a.pitches[root_pitch + ',,']
        while root_frequency < 100.0:
            root_frequency *= 2

        return signal, n_beats, root_frequency, size

    def drone_root(self, fifth=False):

        p_a = st.session_state.p_a

        signal, n_beats, root_frequency, size = self.n_beats_root_pitch()

        t = np.linspace(0, (signal.size - 4 * size) / cst.SAMPLE_RATE, signal.size - 4 * size)

        for h in range(1, 5):
            signal[4 * size:] += np.sin(2.0 * np.pi * t * root_frequency * h) / h ** 2

        if fifth:
            for h in range(1, 5):
                signal[4 * size:] += np.sin(2.0 * np.pi * t * root_frequency * h * 3 / 2) / h ** 2

        signal = self.pulsator(signal, size, t)

        signal /= np.abs(signal).max()
        signal *= (2 ** 15 - 1)

        self.signal = signal.astype(np.int16)

    def pure_chords(self):

        p_a = st.session_state.p_a
        signal, n_beats, root_frequency, size = self.n_beats_root_pitch()
        # number of data points per beat
        dp_per_beat = int(60.0 / self.practice.tempo * cst.SAMPLE_RATE + 0.5)
        self.signal = signal

        previous_duration = 0
        i = 4

        chords = p_a.set_chords()
        start_index = 4 * dp_per_beat
        sample_size = part = t = 0
        for i_durations, durations in enumerate(p_a.lilypond.durations[1:]):
            print(i_durations, durations)
            print(chords[(i_durations // 2) % len(chords)])
            for i_duration, duration in enumerate(durations):
                print("  ", i_duration, duration)
                if duration != previous_duration:
                    previous_duration = duration
                    sample_size = abs(duration) * dp_per_beat // 12
                    t = np.linspace(0, sample_size / cst.SAMPLE_RATE, sample_size)
                    part = np.zeros_like(t)
                part *= 0
                if duration > 0:
                    chord = chords[(i_durations // 2) % len(chords)][i_duration]
                    for note_ratio in chord:
                        for h in range(1, 5):
                            part += np.sin(2 * np.pi * t * root_frequency * h * note_ratio) / h ** 2
                        f = np.linspace(0, 1, 1000)
                        part[:1000] *= f
                        part[-1000:] *= f[::-1]
                signal[start_index:start_index + sample_size] = part
                start_index += sample_size

        signal = signal / np.abs(signal).max()
        self.signal = np.int16(signal * (2 ** 9 - 1))
