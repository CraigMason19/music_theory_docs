# Examples
 
<nav>
  <a href="#scales">Scales</a>
  <a href="#keys">Keys</a>
</nav>

### Scales
To create a scale simply construct a scale class.

```python
scale = Scale(Note.C, ScaleType.Minor)
print(scale)
print(scale.name)
print(scale.notes)
print(scale.num_notes)
print(scale.num_flats)
print(scale.interval_formula)

C Minor: C, D, Eb, F, G, Ab, Bb
C Minor
[Note.C, Note.D, Note.Eb, Note.F, Note.G, Note.Ab, Note.Bb]
7
3
[Interval.Unison, Interval.M2, Interval.m3, Interval.P4, Interval.P5, Interval.m6, Interval.m7]
```

To find all the modes of a note use the modes_from_note function inside scales.py

```python
for mode in modes_from_note(Note.C):
    print(mode)

C Ionian: C, D, E, F, G, A, B
D Dorian: D, E, F, G, A, B, C
E Phrygian: E, F, G, A, B, C, D
F Lydian: F, G, A, B, C, D, E
G Mixolydian: G, A, B, C, D, E, F
A Aeolian: A, B, C, D, E, F, G
B Locrian: B, C, D, E, F, G, A
```

### Keys
To find a list of all chords in a key simply create a Key and use the pretty_print function. e.g.
```python
key = Key(Note.A, KeyType.Major)
key.pretty_print(dominant=True,  parallel=True)

    AM        Bm       Dbm        DM        EM       Gbm     Abdim
     I        ii       iii        IV         V        vi       vii

    E7       Gb7       Ab7        A7        B7       Db7       Eb7
  V7/I     V7/ii    V7/iii     V7/IV      V7/V     V7/vi    V7/vii

    Am      Bdim        CM        Dm        Em        FM        GM
     i        ii       III        iv         v        VI       VII
```

To find the chords of a key from numeral notation use the chords_from_progression function
Note: Uppercase letters & numerals notate major and lowercase notates minor
```python
chords = chords_from_progression(Key(Note.A), ['I', 'ii', 'IV', 'CXIIMII-invalid'])
print(chords)
['AM', 'Bm', 'DM', 'X']
```