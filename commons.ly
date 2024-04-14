\language "deutsch"

Gstring = \markup{\override #'(font-name . "DkgHandwriting") \fontsize #-2 I }
Dstring = \markup{\override #'(font-name . "DkgHandwriting") \fontsize #-2 II }
Astring = \markup{\override #'(font-name . "DkgHandwriting") \fontsize #-2 III }
Estring = \markup{\override #'(font-name . "DkgHandwriting") \fontsize #-2 IV }
Gstring = \markup{ \fontsize #-1 I }
Dstring = \markup{ \fontsize #-1 II }
Astring = \markup{ \fontsize #-1 III }
Estring = \markup{ \fontsize #-1 IV }

pts = \(
% \parenthesize(
pte = \)

fingering =
#(define-music-function
  ( fng )
  ( string? )
  #{
    \finger\markup{
      % \override #'(font-name . "DkgHandwriting")
      \fontsize #2 #fng
    }
  #}
  )

sfingering =
#(define-music-function
  ( fng )
  ( string? )
  #{
    \finger\markup{
      % \override #'(font-name . "DkgHandwriting")
      \fontsize #0 \with-color "grey" #fng
    }
  #}
  )

Nf = \fingering "0"
sNf = \sfingering "0"
% Tf =  \finger\markup{
%   % \override #'(font-name . "DkgHandwriting")
%   \fontsize #3 \char #9792
% }
Tf = \thumb
%Tf = \finger\markup{
%  %\override #'(font-name . "DkgHandwriting")
%  \fontsize #3 \char #9792
%}
sTf = \finger\markup{
  %\override #'(font-name . "DkgHandwriting")
  \fontsize #2 \with-color "grey" \char #9792
}
If = \fingering "1"
sIf = \sfingering "1"
Mf = \fingering "2"
sMf = \sfingering "2"
Rf = \fingering "3"
sRf = \sfingering "3"
Pf = \fingering "4"
sPf = \sfingering "4"

