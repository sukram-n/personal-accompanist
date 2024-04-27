from importlib import reload
import uuid

import personal_accompanist.lilypond as lilypond
import personal_accompanist.audio as audio
import personal_accompanist.widgets as widgest
import constants as cst

reload(lilypond)
reload(audio)
reload(widgets)
reload(cst)


class PersonalAccompanist:

    def __init__(self):

        self.initial_run = True
        self.basename = uuid.uuid4().hex
        self.total_durations = []
        self.key = 'C'
        self.speeds = []
        self.tempo = 60
        self.exercise = 'One Octave'
        self.loop = False
        self.acc_instr = 'Grand Piano (well tempered)'
        self.reference_pitch = cst.REFERENCE_PITCH
        self.audio_signal = None

        self.lilypond = lilypond.LilyPond()
        self.audio = audio.Audio()
        self.widgets = widgest.Widgets()

    @property
    def key_text(self):
        if self.key[0].isupper():
            return self.key + '-major'
        else:
            return self.key + '-minor'
