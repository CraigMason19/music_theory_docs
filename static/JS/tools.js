// Tool 1
const chordsInKeyForm = document.getElementById("chords-in-key-form");

const toolOneNoteInput = document.getElementById("tool-one-note-input");
const toolOneKeyTypeInput = document.getElementById("tool-one-key-type-input");
const toolOneDominantInput = document.getElementById("tool-one-dominant-input");

toolOneNoteInput.addEventListener("change", () => {
    chordsInKeyForm.submit()
});

toolOneKeyTypeInput.addEventListener("change", () => {
    chordsInKeyForm.submit()
});

toolOneDominantInput.addEventListener("change", () => {
    chordsInKeyForm.submit()
});


// Tool 2
const modesFromNoteForm = document.getElementById("modes-from-note-form");

const toolTwoNoteInput = document.getElementById("tool-two-note-input");





toolTwoNoteInput.addEventListener("change", () => {
    modesFromNoteForm.submit()
});