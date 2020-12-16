\version "2.18.2"

#(set! paper-alist (cons '("snippet" . (cons (* 20 mm) (* 20 mm))) paper-alist))
\paper {
  #(set-paper-size "snippet")
  indent = 0
  tagline = ##f
  print-all-headers = ##f
  evenHeaderMarkup = ##f
  oddHeaderMarkup = ##f
  evenFooterMarkup = ##f
  oddFooterMarkup = ##f
  % top-margin = 1\mm
  top-markup-spacing.basic-distance = #0 %-dist. from bottom of top margin to the first markup/title
  markup-system-spacing.basic-distance = #0 %-dist. from header/title to first system
  top-system-spacing.basic-distance = 01 %-dist. from top margin to system in pages with no titles
  system-system-spacing.basic-distance = #0 %-dist. from top margin to system in pages with no titles
  last-bottom-spacing.basic-distance = #0 %-pads music from copyright block
}

\score {
  {
    \omit Staff.TimeSignature
    \override Score.BarLine.break-visibility = #all-invisible
    \set Staff.explicitClefVisibility = #begin-of-line-visible
    \clef treble \relative c' { <d f>1 }
    \pageBreak
    \clef bass \relative c { <geses des'>1 }
    \pageBreak
    \clef treble \relative c' { <ais g''>1 }
  }
  \layout {
    \context {
      \Score
      \omit BarNumber
    }
  }
}
