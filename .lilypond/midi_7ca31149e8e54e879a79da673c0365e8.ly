\version "2.24.1"
\language "english"
\include "./../lilypond/commons.ly"

piano = \new Staff \with {midiInstrument = "acoustic grand" } {
 \accidentalStyle modern-cautionary
 \tupletDown
 \override TextScript.staff-padding = # 3
 \key b-flat \minor
 \clef "bass_8"
 \tempo 4=175 
r1 b-flat,,2^\If c,2^\Mf d-flat,2 e-flat,2^\If f,2 g,2^\Nf a,2 b-flat,2 a-flat,2 g-flat,2^\Pf f,2 e-flat,2^\Pf_\Astring d-flat,2 c,2^\Pf b-flat,,2 r2 \bar "||"
 b-flat,,4^\If c,4^\Mf d-flat,4 e-flat,4^\If f,4 g,4^\Nf a,4 b-flat,4 a-flat,4 g-flat,4^\Pf f,4 e-flat,4^\Pf_\Astring d-flat,4 c,4^\Pf b-flat,,4 r4 \bar "|."

}
metronome = \new Staff \with {midiInstrument = "woodblock" } {
c4 c4 c4 c4 
 r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  \bar  "||"
 r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  \bar  "|."

}

\book {
  \bookOutputName "midi_7ca31149e8e54e879a79da673c0365e8"
  \header{ tagline = "" }
  \score {
    <<
        \piano
        \metronome
      >>
    \midi { }
  }
}