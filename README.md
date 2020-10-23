# Tutorial for identifying written music interval (ABRSM Grade 5 music theory)

## Setup

```bash
pip install -r requirements
```

Set the policy for ImageMagick by commenting the lines in the section of `/etc/ImageMagick-7/policy.xml`

```
<!-- disable ghostscript format types -->
```

Reference: https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion

Also, comment out:

```
<policy domain="path" rights="none" pattern="@*" />
```

Reference: https://github.com/Zulko/moviepy/issues/693#issuecomment-355587113

## Script/Content

How to identify interval in 3 steps

Step 1: Count to get the number:
Count the number of notes (inclusive) ignoring accidentals. Use "compound" for exceeding an octave"

Example 1: D to F -> 3 (D, E, F) [Highlight first 4 words]

Example 2: Gbb to Db -> 5 (G, A, B, C, D) (highlight also ignoring accidentals)

Example 3: A# to higher G -> compound 7 (A, B, C, D, E, F, G)

Exercise 1: E to C
Exercise 2: F# to Db
Exercise 3: C to high F#

Step 2: Find the note to compare:
Write down the major scale from the lower note, and find the n-th note obtained from step 1

Example 1: D major scale: D, E, F#, G, ... 3rd note is F#
Example 2: Gbb (F) major scale: F, G, A, Bb, C, D, ... 5th note is C. [You are not comparing with D!]
Example 3: A# (Bb) major scale: Bb, C, D, Eb, F, G, A ... 7th note is A [You are not comparing with G!].

Step 3: compare the note in step 2 with the higher note in the question:

Same (The baseline)
```
1,      4, 5,      8 -> Perfect
   2, 3,      6, 7   -> Major
```
The adjustment line is:
Diminished -> Perfect -> Augmented, or
Diminished -> Minor -> Major -> Augmented

Example 1: F is one semitone lower than F#, and the baseline (for 3 notes) is Major. Therefore it shifts from Major down to Minor. Answer: Minor 3rd.

Example 2: Db is one semitone higher than C, and the baseline (for 5 notes) is Perfect. Therefore it shifts from Perfect up to Augmented. Answer: Augmented 5th.

Example 3: G is 2 semitones lower than A, and the baseline (for 7 notes) is Major. Therefore it shifts from Major down 2 steps to Diminished. Answer: Compound diminished 7th.

Final Words:
Do not adopt any methods on counting the total number of semitones! They are simply not the right way to count and interpret intervals, and do not help interpreting music nor understanding music theories.
