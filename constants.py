EXERCISES = ['one octave', 'two octaves', 'triads']

EVENT_VALUES = {'1whole notes': (1, 1),
          '2half notes': (2, 2),
          '3quarter notes': (4, 4),
          '4eigth notes': (8, 8),
          '5eigth triplets': (12, 8),
          '6sixteenth': (16, 16)}

TRANSLATIONS = {
    "0": "\\Nf",
    "1": "\\If",
    "2": "\\Mf",
    "3": "\\Rf",
    "4": "\\Pf",
    "t": "\\Tf",
    "-": "",
    "B": '\\clef "bass_8"\n',
    "T": '\\clef "tenor_8"\n',
    "V": '\\clef "violin_8"\n',
    "G": "_\\Gstring\n",
    "D": "_\\Dstring\n",
    "A": "_\\Astring\n",
    "E": "_\\Estring\n",
}


HEAD = f"""\\version "2.22.1"
\\language "deutsch"
\\include "commons.ly"

"""
