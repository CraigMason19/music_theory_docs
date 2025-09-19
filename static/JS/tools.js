// Tool 1
const chordsInKeyForm = document.getElementById("chords-in-key-form");

const toolOneNoteInput = document.getElementById("tool-one-note-input");
const toolOneKeyTypeInput = document.getElementById("tool-one-key-type-input");
const toolOneDominantInput = document.getElementById("tool-one-dominant-input");
const toolOneParallelInput = document.getElementById("tool-one-parallel-input");

const inputs = [
    toolOneNoteInput,
    toolOneKeyTypeInput,
    toolOneDominantInput,
    toolOneParallelInput,
]

inputs.forEach(i => {
    i.addEventListener("change", () => {
        chordsInKeyForm.submit()
    });
});



// Tool 2
const modesFromNoteForm = document.getElementById("modes-from-note-form");

const toolTwoNoteInput = document.getElementById("tool-two-note-input");





toolTwoNoteInput.addEventListener("change", () => {
    modesFromNoteForm.submit()
});