#(ly:font-config-add-directory ".fonts")

% #(ly:font-config-display-fonts)

Gstring = \markup{ \hspace #-0.1 \override #'(font-name . "DkgHandwriting") \fontsize #+0 I }
Dstring = \markup{\hspace #-0.2 \override #'(font-name . "DkgHandwriting") \fontsize #+0 II }
Astring = \markup{\hspace #-0.5 \override #'(font-name . "DkgHandwriting") \fontsize #+0 III }
Estring = \markup{\hspace #-0.3 \override #'(font-name . "DkgHandwriting") \fontsize #+0 IV }


pts = \(
% \parenthesize(
pte = \)

Nf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 0 }
sNf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 \with-color "grey" 0
}

Tf = \markup{
  \hspace #-0.1
  % \override #'(font-name . "DkgHandwriting")
  \fontsize #+0  \char #9792
}
sTf = \markup{
  \hspace #-0.1
  % \override #'(font-name . "DkgHandwriting")
  \fontsize #+0 \with-color "grey" \char #9792
}

If = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 1
}

sIf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 \with-color "grey" 1
}
Mf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 2
}
sMf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 \with-color "grey" 2
}
Rf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 3
}
sRf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 \with-color "grey" 3
}
Pf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 4
}
sPf = \markup{
  \hspace #-0.1
  \override #'(font-name . "DkgHandwriting") \fontsize #+0 \with-color "grey" 4
}
