\version "2.24.1"
\language "english"
\include "./../lilypond/commons.ly"

piano = \new Staff \with {midiInstrument = "acoustic grand" } {
 \accidentalStyle modern-cautionary
 \tupletDown
 \override TextScript.staff-padding = # 3
 \key b-flat \minor
 \clef "bass_8"
 \tempo 4=70 
r1 b-flat,,1^\If c,1^\Mf d-flat,1 e-flat,1^\If f,1 g,1^\Nf a,1 b-flat,1 c1^\Mf d-flat1 \clef "tenor_8"
e-flat1^\If f1 g1^\Tf a1^\If b-flat1 a-flat1^\If g-flat1^\Pf f1 e-flat1^\Pf d-flat1 c1^\Pf b-flat,1 \clef "bass_8"
a-flat,1^\Pf_\Dstring  g-flat,1 f,1^\Pf e-flat,1 d-flat,1^\Pf c,1 b-flat,,1^\If r1 \bar "||"
 b-flat,,2^\If\( c,2^\Mf\) d-flat,2\( e-flat,2^\If\) f,2\( g,2^\Nf\) a,2\( b-flat,2\) c2^\Mf\( d-flat2\) \clef "tenor_8"
e-flat2^\If\( f2\) g2^\Tf\( a2^\If\) b-flat2\( a-flat2^\If\) g-flat2^\Pf\( f2\) e-flat2^\Pf\( d-flat2\) c2^\Pf\( b-flat,2\) \clef "bass_8"
a-flat,2^\Pf_\Dstring \( g-flat,2\) f,2^\Pf\( e-flat,2\) d-flat,2^\Pf\( c,2\) b-flat,,2^\If r2 \bar "||"
 b-flat,,4^\If\( c,4^\Mf d-flat,4 e-flat,4^\If\) f,4\( g,4^\Nf a,4 b-flat,4\) c4^\Mf\( d-flat4 \clef "tenor_8"
e-flat4^\If f4\) g4^\Tf\( a4^\If b-flat4 a-flat4^\If\) g-flat4^\Pf\( f4 e-flat4^\Pf d-flat4\) c4^\Pf\( b-flat,4 \clef "bass_8"
a-flat,4^\Pf_\Dstring g-flat,4\) f,4^\Pf\( e-flat,4 d-flat,4^\Pf c,4\) b-flat,,4^\If r4 r2 \bar "||"
 b-flat,,8^\If\( c,8^\Mf d-flat,8 e-flat,8^\If f,8 g,8^\Nf a,8 b-flat,8\) c8^\Mf\( d-flat8 \clef "tenor_8"
e-flat8^\If f8 g8^\Tf a8^\If b-flat8 a-flat8^\If\) g-flat8^\Pf\( f8 e-flat8^\Pf d-flat8 c8^\Pf b-flat,8 \clef "bass_8"
a-flat,8^\Pf_\Dstring g-flat,8\) f,8^\Pf\( e-flat,8 d-flat,8^\Pf c,8 b-flat,,8^\If\) r8 r4 \bar "||"
 \tuplet 3/2 {b-flat,,8^\If\( c,8^\Mf d-flat,8} \tuplet 3/2 {e-flat,8^\If f,8 g,8^\Nf} \tuplet 3/2 {a,8 b-flat,8 c8^\Mf} \tuplet 3/2 {d-flat8 \clef "tenor_8"
e-flat8^\If f8\)} \tuplet 3/2 {g8^\Tf\( a8^\If b-flat8} \tuplet 3/2 {a-flat8^\If g-flat8^\Pf f8} \tuplet 3/2 {e-flat8^\Pf d-flat8 c8^\Pf} \tuplet 3/2 {b-flat,8 \clef "bass_8"
a-flat,8^\Pf_\Dstring g-flat,8\)} \tuplet 3/2 {f,8^\Pf\( e-flat,8 d-flat,8^\Pf} \tuplet 3/2 {c,8 b-flat,,8^\If\) r8} r2 \bar "||"
 b-flat,,16^\If\( c,16^\Mf d-flat,16 e-flat,16^\If f,16 g,16^\Nf a,16 b-flat,16 c16^\Mf d-flat16 \clef "tenor_8"
e-flat16^\If f16 g16^\Tf a16^\If b-flat16 a-flat16^\If\) g-flat16^\Pf\( f16 e-flat16^\Pf d-flat16 c16^\Pf b-flat,16 \clef "bass_8"
a-flat,16^\Pf_\Dstring g-flat,16 f,16^\Pf e-flat,16 d-flat,16^\Pf c,16 b-flat,,16^\If\) r16 r8 \bar "|."

}
metronome = \new Staff \with {midiInstrument = "woodblock" } {
c4 c4 c4 c4 
 r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  r1  \bar  "||"
 r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  r2  \bar  "||"
 r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  r4  \bar  "||"
 r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  \bar  "||"
 r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  r8  \bar  "||"
 r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  r16  \bar  "|."

}

\book {
  \bookOutputName "svg_7ca31149e8e54e879a79da673c0365e8"
  \header{ tagline = "" }
  \score {
    << \piano >>
    \layout{ indent = 0 }
  }
}