## 1 - Activate venv in powershel
.\.venv\Scripts\Activate.ps1

## 2 - Activate server
python manage.py runserver

## 3 - go to
http://127.0.0.1:8000/documentation/
## or
http://127.0.0.1:8000

## If doing CSS CTRL + F5




## Links
https://github.com/CraigMason19
 
https://CraigMason19.github.io/music_theory_docs/

pip install git+https://github.com/CraigMason19/music_theory

python manage.py runserver
http://127.0.0.1:8000/documentation/


## Making Changes in music_theory
- Update the package
- Bake down into static content











next step

https://craigmason19.github.io/music_theory_docs 
is index.html

so i need to design / hook up documentation

if i make a change i have to 'bake' dynamic content down to static for github

django-distill













Here’s how your proposed apps break down:

documentation/ Handles introspection of your Python package, parsing docstrings, and rendering readable content. Think of it as the book spine.

midi_exporter/ Encodes progressions, scales, or custom harmonic shapes into MIDI files. This is the utility shop for sound artifacts.

viewer/ Could be the visual layer — rendering chords, interval graphs, key relationships, etc. Possibly powered by D3 or some canvas logic.

And if you want to go even further:

progression_lab/ An experimental module to generate, mutate, and analyze chord progressions.

notational_tools/ For rendering staves, naming conventions, symbol mappings (especially if you go SATB or modal).

bake_engine/ (optional) Centralized module that orchestrates static page rendering from other apps.


 